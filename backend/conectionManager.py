from fastapi import WebSocket
import json
from backend.redis import r
import asyncio

class ConectionManager:
    def __init__(self):
        # WebSocket-подключения хранятся по стабильному id игрока.
        self.active_connections: dict[int, WebSocket] = {}

        # В памяти держим последнюю позицию каждого подключенного игрока.
        self.positions: dict[int, dict] = {}

        # Счетчик id всегда растет, чтобы id не пересекались при отключениях.
        self._next_player_id: int = 1

        # Один фоновый цикл рассылает snapshot-пакеты всем клиентам.
        self._broadcast_task: asyncio.Task | None = None

        # Lock защищает общие словари от одновременного изменения.
        self._lock = asyncio.Lock()
    
    async def connect(self, websocket: WebSocket) -> int:
        async with self._lock:
            # Выдаем id на весь срок жизни этого websocket-подключения.
            player_id = self._next_player_id
            self._next_player_id += 1
            self.active_connections[player_id] = websocket

            # Запускаем фоновую рассылку, когда подключился первый клиент.
            if self._broadcast_task is None or self._broadcast_task.done():
                self._broadcast_task = asyncio.create_task(self.broadcast_loop())

        return player_id

    async def disconnect(self, player_id: int) -> None:
        async with self._lock:
            # Удаляем все состояние игрока на стороне сервера.
            self.active_connections.pop(player_id, None)
            self.positions.pop(player_id, None)
    
    def getCount(self) -> int:
        return len(self.active_connections)

    async def update_position(self, player_id: int, coords: dict) -> None:
        # Сохраняем самую новую позицию в памяти для быстрой рассылки.
        async with self._lock:
            self.positions[player_id] = coords

        # Redis хранит последнее состояние, а не всю историю движений.
        await r.hset("players:positions", player_id, json.dumps(coords))

    async def broadcast_loop(self) -> None:
        tick = 0

        while True:
            # Рассылаем snapshot с фиксированной частотой, а не каждое движение отдельно.
            await asyncio.sleep(1 / 30)
            tick += 1

            async with self._lock:
                # Копируем общее состояние перед отправкой, чтобы не держать lock во время send.
                connections = list(self.active_connections.items())
                positions = [
                    {"id": player_id, **coords}
                    for player_id, coords in self.positions.items()
                ]

            if not connections:
                continue

            disconnected_ids: list[int] = []

            for player_id, websocket in connections:
                # Не отправляем игроку его же собственную позицию обратно.
                payload = json.dumps({
                    "type": "snapshot",
                    "tick": tick,
                    "players": [
                        position
                        for position in positions
                        if position["id"] != player_id
                    ]
                })

                try:
                    await websocket.send_text(payload)
                except Exception as ex:
                    print(f"Broadcast error for player {player_id}: {ex}")
                    disconnected_ids.append(player_id)

            # Чистим подключения, которым не удалось отправить сообщение.
            for player_id in disconnected_ids:
                await self.disconnect(player_id)
