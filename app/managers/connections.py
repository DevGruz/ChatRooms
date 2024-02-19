from fastapi import WebSocket


class WSConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, data: str, websocket: WebSocket):
        await websocket.send_text(data)

    async def broadcast(self, data: str):
        for connection in self.active_connections:
            await connection.send_text(data)


connection_manager = WSConnectionManager()
