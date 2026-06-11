from datetime import datetime
from fastapi import FastAPI

from app.api.websocket import router as websocket_router
from app.api.front_endpoints import router as front_endpoints_router

app = FastAPI()

START_TIME = datetime.now()

app.include_router(websocket_router)

app.include_router(front_endpoints_router)