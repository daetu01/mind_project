import httpx
import os
import base64
from dotenv import load_dotenv

load_dotenv()

class BattleNetService:
    def __init__(self):
        self.client_id = os.getenv("BNET_CLIENT_ID")
        self.client_secret = os.getenv("BNET_CLIENT_SECRET")
        self.region = os.getenv("BNET_REGION", "kr")
        self.access_token = None

    async def get_access_token(self):
        if self.access_token:
            return self.access_token

        auth = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        url = "https://oauth.battle.net/token"

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                data={"grant_type": "client_credentials"},
                headers={
                    "Authorization": f"Basic {auth}",
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            )
            response.raise_for_status()
            self.access_token = response.json()["access_token"]
            return self.access_token

    async def get_character_profile(self, realm: str, character_name: str):
        token = await self.get_access_token()
        url = f"https://{self.region}.api.blizzard.com/profile/wow/character/{realm}/{character_name.lower()}?namespace=profile-{self.region}&locale=ko_KR"

        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return response.json()

    async def get_character_equipment(self, realm: str, character_name: str):
        token = await self.get_access_token()
        url = f"https://{self.region}.api.blizzard.com/profile/wow/character/{realm}/{character_name.lower()}/equipment?namespace=profile-{self.region}&locale=ko_KR"

        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return response.json()

    async def get_character_stats(self, realm: str, character_name: str):
        token = await self.get_access_token()
        url = f"https://{self.region}.api.blizzard.com/profile/wow/character/{realm}/{character_name.lower()}/statistics?namespace=profile-{self.region}&locale=ko_KR"

        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return response.json()

    async def get_character_specializations(self, realm: str, character_name: str):
        token = await self.get_access_token()
        url = f"https://{self.region}.api.blizzard.com/profile/wow/character/{realm}/{character_name.lower()}/specializations?namespace=profile-{self.region}&locale=ko_KR"

        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return response.json()

    async def get_auctions(self, connected_realm_id: int):
        token = await self.get_access_token()
        url = f"https://{self.region}.api.blizzard.com/data/wow/connected-realm/{connected_realm_id}/auctions?namespace=dynamic-{self.region}&locale=ko_KR"

        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return response.json()

    async def get_item_info(self, item_id: int):
        token = await self.get_access_token()
        url = f"https://{self.region}.api.blizzard.com/data/wow/item/{item_id}?namespace=static-{self.region}&locale=ko_KR"

        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return response.json()

    async def get_connected_realm_id(self, realm_name: str):
        # Cache-able mapper or dynamic search
        token = await self.get_access_token()
        url = f"https://{self.region}.api.blizzard.com/data/wow/search/connected-realm"
        params = {
            "namespace": f"dynamic-{self.region}",
            "realms.name.ko_KR": realm_name,
            "locale": "ko_KR"
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers={"Authorization": f"Bearer {token}"},
                params=params
            )
            response.raise_for_status()
            data = response.json()
            if data.get("results"):
                return data["results"][0]["data"]["id"]
            return None

    async def get_mythic_leaderboard_index(self, connected_realm_id: int):
        token = await self.get_access_token()
        url = f"https://{self.region}.api.blizzard.com/data/wow/connected-realm/{connected_realm_id}/mythic-leaderboard/index?namespace=dynamic-{self.region}&locale=ko_KR"

        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return response.json()

    async def get_mythic_leaderboard(self, connected_realm_id: int, dungeon_id: int, period_id: int):
        token = await self.get_access_token()
        url = f"https://{self.region}.api.blizzard.com/data/wow/connected-realm/{connected_realm_id}/mythic-leaderboard/{dungeon_id}/period/{period_id}?namespace=dynamic-{self.region}&locale=ko_KR"

        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return response.json()

bnet_service = BattleNetService()
