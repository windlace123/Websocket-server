from datetime import datetime
from fastapi import APIRouter
import asyncio
import json

router = APIRouter()

START_TIME = datetime.now()

@router.post("/server_stats")
async def server_stats():
    server_all_stats: dict = {}

    server_all_stats["uptime"] = datetime.now() - START_TIME

    await asyncio.sleep(0.5)

    return json.dumps(server_all_stats)