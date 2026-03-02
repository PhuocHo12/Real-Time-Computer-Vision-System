import asyncio

class WebSocketManager:
    def __init__(self):
        self.connections = set()
        self.lock = asyncio.Lock()

    async def connect(self, websocket):
        await websocket.accept()
        async with self.lock:
            self.connections.add(websocket)

    async def disconnect(self, websocket):
        async with self.lock:
            self.connections.discard(websocket)

    async def broadcast(self, message: str):
        async with self.lock:
            dead = []
            for ws in self.connections:
                try:
                    await ws.send_text(message)
                except Exception:
                    dead.append(ws)

            for ws in dead:
                self.connections.discard(ws)