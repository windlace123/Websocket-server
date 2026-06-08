from fastapi import APIRouter, WebSocket

from backend.app.core.redis_client import r
from backend.app.db.database import Database
from backend.app.schemas.player import parse_position_message
from backend.app.services.connection_manager import ConnectionManager

router = APIRouter()
db = Database()
connection_manager = ConnectionManager()


@router.websocket("/ws")
async def handler(websocket: WebSocket) -> None:
    player_id: int | None = None

    try:
        await websocket.accept()
        player_id = await connection_manager.connect(websocket)

        client = websocket.client
        db.add_player(
            player_id=player_id,
            host=client.host if client else "",
            port=client.port if client else 0,
        )

        print(f"User Connected: {player_id}")

        while True:
            data = await websocket.receive_text()
            coords = parse_position_message(data)
            await connection_manager.update_position(player_id, coords)

    except Exception as exc:
        print(f"Error: {exc}")

    finally:
        if player_id is not None:
            db.delete_player(player_id)
            await r.hdel("players:positions", player_id)
            await connection_manager.disconnect(player_id)

        print(f"User Disconnected: {player_id}")
