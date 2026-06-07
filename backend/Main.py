from fastapi import FastAPI, WebSocket
import json
from backend.database import Database
from backend.conectionManager import ConectionManager
from backend.redis import r

app: FastAPI = FastAPI()
db = Database()

connManager = ConectionManager()

def strToDict(message: str) -> dict:
    # Сначала пробуем новый JSON-формат, но старый текстовый формат тоже поддерживаем.
    try:
        data = json.loads(message)
        if data.get("type") == "pos":
            return {
                "x": float(data["x"]),
                "y": float(data["y"]),
                "z": float(data["z"])
            }

        return {
            "x": float(data["x"]),
            "y": float(data["y"]),
            "z": float(data["z"])
        }
    except json.JSONDecodeError:
        pass

    # Старый формат клиента: x:10.5,y:2.0,z:-4.2
    parts: list[str] = message.split(',')
    coords: dict = {
        'x': float(parts[0].split(':')[1]),
        'y': float(parts[1].split(':')[1]),
        'z': float(parts[2].split(':')[1])
    }

    return coords


@app.websocket("/ws")
async def handler(websocket: WebSocket):
    player_id: int | None = None

    try:
        await websocket.accept()

        # Менеджер соединений сам выдает стабильный id игрока.
        player_id = await connManager.connect(websocket)

        db.addPlayer(
            player_id,
            websocket.client.host,
            websocket.client.port
        )

        # Отправляем клиенту id, который сервер назначил этому подключению.
        # await websocket.send_text(json.dumps({
        #     "type": "welcome",
        #     "id": player_id
        # }))

        print(f"User Connected: {player_id}")

        while True:
            # Каждое входящее сообщение обновляет только последнюю известную позицию.
            data: str = await websocket.receive_text()
            coords: dict = strToDict(data)
            await connManager.update_position(player_id, coords)

    except Exception as ec:
        print(f"Error: {ec}")
    
    finally:
        if player_id is not None:
            # Удаляем отключившегося игрока из базы, Redis и памяти сервера.
            db.delPlayer(player_id)
            await r.hdel("players:positions", player_id)
            await connManager.disconnect(player_id)

        print(f"User Disconnected: {player_id}")
