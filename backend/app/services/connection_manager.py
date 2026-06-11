import asyncio
import json

from fastapi import WebSocket

from app.core.redis_client import r
from app.schemas.player import Position


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: dict[int, WebSocket] = {}
        self.positions: dict[int, Position] = {}
        self._next_player_id = 1
        self._broadcast_task: asyncio.Task | None = None
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket) -> int:
        async with self._lock:
            player_id = self._next_player_id
            self._next_player_id += 1
            self.active_connections[player_id] = websocket

            if self._broadcast_task is None or self._broadcast_task.done():
                self._broadcast_task = asyncio.create_task(self.broadcast_loop())

        return player_id

    async def disconnect(self, player_id: int) -> None:
        async with self._lock:
            self.active_connections.pop(player_id, None)
            self.positions.pop(player_id, None)

    def get_count(self) -> int:
        return len(self.active_connections)

    async def update_position(self, player_id: int, coords: Position) -> None:
        async with self._lock:
            self.positions[player_id] = coords

        await r.hset("players:positions", player_id, json.dumps(coords))

    async def broadcast_loop(self) -> None:
        tick = 0

        while True:
            await asyncio.sleep(1 / 30)
            tick += 1

            async with self._lock:
                connections = list(self.active_connections.items())
                positions = [
                    {"id": player_id, **coords}
                    for player_id, coords in self.positions.items()
                ]

            if not connections:
                continue

            disconnected_ids: list[int] = []

            for player_id, websocket in connections:
                payload = json.dumps(
                    {
                        "type": "snapshot",
                        "tick": tick,
                        "players": [
                            position
                            for position in positions
                            if position["id"] != player_id
                        ],
                    }
                )

                try:
                    await websocket.send_text(payload)
                except Exception as exc:
                    print(f"Broadcast error for player {player_id}: {exc}")
                    disconnected_ids.append(player_id)

            for player_id in disconnected_ids:
                await self.disconnect(player_id)
