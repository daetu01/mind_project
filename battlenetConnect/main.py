from fastapi import FastAPI, HTTPException
from services.battlenet import bnet_service
from services.processor import processor
from services.auction_processor import auction_processor
from services.leaderboard_processor import leaderboard_processor
from services.storage import storage
import uvicorn

app = FastAPI(title="WoW Data Pipeline API")

@app.get("/character/{realm}/{name}")
async def get_character_data(realm: str, name: str):
    try:
        # 1. Fetch data from Battle.net
        profile = await bnet_service.get_character_profile(realm, name)
        equipment = await bnet_service.get_character_equipment(realm, name)
        stats = await bnet_service.get_character_stats(realm, name)
        specs = await bnet_service.get_character_specializations(realm, name)
        
        # 2. Process and refine
        refined_data = processor.process(profile, equipment, stats, specs)
        
        # 3. Save to local JSON
        storage.save("character", f"{realm}_{name}", refined_data)
        
        return refined_data
    except Exception as e:
        return {"error": str(e)}

@app.get("/auctions/{realm}")
async def get_auctions(realm: str):
    try:
        # 1. Find connected realm ID
        connected_realm_id = await bnet_service.get_connected_realm_id(realm)
        if not connected_realm_id:
            return {"error": f"Realm '{realm}' not found."}
        
        # 2. Fetch AH data
        auctions_data = await bnet_service.get_auctions(connected_realm_id)
        
        # 3. Process
        refined = auction_processor.process(auctions_data)
        
        # 4. Save to local JSON
        storage.save("auctions", realm, refined)
        
        return refined
    except Exception as e:
        return {"error": str(e)}

@app.get("/leaderboard/{realm}/index")
async def get_leaderboard_index(realm: str):
    try:
        connected_realm_id = await bnet_service.get_connected_realm_id(realm)
        if not connected_realm_id:
            return {"error": f"Realm '{realm}' not found."}
        
        index = await bnet_service.get_mythic_leaderboard_index(connected_realm_id)
        return index
    except Exception as e:
        return {"error": str(e)}

@app.get("/leaderboard/{realm}/{dungeon_id}/{period_id}")
async def get_leaderboard_data(realm: str, dungeon_id: int, period_id: int):
    try:
        connected_realm_id = await bnet_service.get_connected_realm_id(realm)
        if not connected_realm_id:
            return {"error": f"Realm '{realm}' not found."}
        
        data = await bnet_service.get_mythic_leaderboard(connected_realm_id, dungeon_id, period_id)
        refined = leaderboard_processor.process(data)
        
        # Save to local JSON
        dungeon_name = refined.get("던전명", f"dungeon_{dungeon_id}")
        storage.save("leaderboard", f"{realm}_{dungeon_name}", refined)
        
        return refined
    except Exception as e:
        return {"error": str(e)}

@app.get("/item/{item_id}")
async def get_item_detail(item_id: int):
    try:
        item_info = await bnet_service.get_item_info(item_id)
        return item_info
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
