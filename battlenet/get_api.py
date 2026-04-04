from fastapi import FastAPI, HTTPException
import requests
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware # 추가
load_dotenv() # .env 파일을 읽어서 환경 변수로 등록해줌

app = FastAPI()

# 1. 허용할 도메인 목록 (리액트나 뷰 서버 주소)
origins = [
    "http://localhost:5173",  # Vite 기본 포트
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 환경 변수 체크 (없으면 에러 발생)
CLIENT_ID = os.getenv("BATTLENET_CLIENT_ID")
CLIENT_SECRET = os.getenv("BATTLENET_CLIENT_SECRET")

# 전역 변수에 토큰 임시 저장 (간이 캐싱)
_cached_token = None

def get_access_token():
    global _cached_token
    if _cached_token:
        return _cached_token
    
    # 한국 리전으로 변경
    url = "https://kr.battle.net/oauth/token"
    data = {"grant_type": "client_credentials"}
    
    try:
        response = requests.post(url, data=data, auth=(CLIENT_ID, CLIENT_SECRET))
        response.raise_for_status()
        _cached_token = response.json().get("access_token")
        return _cached_token
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OAuth 인증 실패: {str(e)}")

def _fetch_href_json(href: str, token: str):
    if not href or not isinstance(href, str):
        return None

    headers = {
        "Authorization": f"Bearer {token}",
        "Battlenet-Namespace": "profile-kr",
    }

    try:
        res = requests.get(href, headers=headers, params={"locale": "ko_KR"})
        if res.status_code == 404:
            return {"error": "not_found", "href": href}
        res.raise_for_status()
        return res.json()
    except Exception as e:
        return {"error": str(e), "href": href}

@app.get("/wow/character/{realm}/{name}")
def get_wow_character(realm: str, name: str):
    token = get_access_token()
    if not token:
        raise HTTPException(status_code=401, detail="토큰을 가져올 수 없습니다.")

    # 1. 서버 슬러그와 이름을 소문자로 처리
    realm_slug = realm.lower()
    char_name = name.lower()

    # 2. API 호출 주소 (URL에 한글이 들어갈 경우 requests가 처리하지만 안전하게 구성)
    url = f"https://kr.api.blizzard.com/profile/wow/character/{realm_slug}/{char_name}"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Battlenet-Namespace": "profile-kr" # 헤더로 넣는 것이 더 표준적입니다.
    }
    params = {
        "locale": "ko_KR"
    }

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 404:
        return {"error": "캐릭터를 찾을 수 없습니다. 오랫동안 접속하지 않았거나 이름이 틀렸을 수 있습니다."}
        
    return response.json()

@app.get("/wow/character-bundle/{realm}/{name}")
def get_wow_character_bundle(realm: str, name: str):
    token = get_access_token()
    if not token:
        raise HTTPException(status_code=401, detail="토큰을 가져올 수 없습니다.")

    summary = get_wow_character(realm, name)
    if isinstance(summary, dict) and summary.get("error"):
        return summary

    equipment_href = (summary.get("equipment") or {}).get("href")
    statistics_href = (summary.get("statistics") or {}).get("href")
    specializations_href = (summary.get("specializations") or {}).get("href")
    mythic_keystone_profile_href = (summary.get("mythic_keystone_profile") or {}).get("href")

    return {
        "summary": summary,
        "equipment": _fetch_href_json(equipment_href, token),
        "statistics": _fetch_href_json(statistics_href, token),
        "specializations": _fetch_href_json(specializations_href, token),
        "mythic_keystone_profile": _fetch_href_json(mythic_keystone_profile_href, token),
    }

@app.get("/wow/rio/{realm}/{name}")
def get_mythic_score(realm: str, name: str):
    token = get_access_token()
    url = f"https://kr.api.blizzard.com/profile/wow/character/{realm.lower()}/{name.lower()}/mythic-keystone-profile"
    headers = {
        "Authorization": f"Bearer {token}",
        "Battlenet-Namespace": "profile-kr"
    }

    res = requests.get(url, headers=headers, params={"locale": "ko_KR"})
    data = res.json()

    # 점수만 쏙 뽑아서 리턴
    return {
        "name": name, 
        "score": data.get("current_mythic_rating", {}).get("rating", 0) # 점수가 없으면 0으로 처리  
    }

@app.get("/wow/character-card/{realm}/{name}")
def get_character_card(realm:str, name:str):
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}", "Battlenet-Namespace": "profile-kr"}
    params = {"locale": "ko_KR"}

    # 1. 캐릭터 기본 정보 가져오기
    summary_url = f"https://kr.api.blizzard.com/profile/wow/character/{realm.lower()}/{name.lower()}"
    summary_res = requests.get(summary_url, headers=headers, params=params)
    if summary_res.status_code != 200:
        raise HTTPException(status_code=404, detail="캐릭터를 찾을 수 없습니다.")
    summary_data = summary_res.json()

    # 2. 캐릭터 미디어(이미지) 정보 가져오기
    media_url = summary_data["media"]["href"]
    media_res = requests.get(media_url, headers=headers) # 이미 href에 namespace가 포함되어 있음
    media_data = media_res.json()

    # 3. 이미지 리스트에서 필요한 것만 추출 (보통 avatar, main, inset 등이 있음)
    images = {}
    for asset in media_data.get("assets", []):
        images[asset["key"]] = asset["value"]

    # 4. 결과 합치기 (이름, 레벨, 직업, 아이템레벨 + 이미지)
    return {
        "name": summary_data["name"],
        "level": summary_data["level"],
        "class": summary_data["character_class"]["name"],
        "spec": summary_data["active_spec"]["name"],
        "item_level": summary_data["equipped_item_level"],
        "images": images  # 여기서 이미지가 튀어나옵니다!
    }