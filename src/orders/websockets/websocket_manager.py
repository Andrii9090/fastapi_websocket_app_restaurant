from fastapi import WebSocket, websockets


class WebSocketManager:
    instance = None

    clients = None

    def __init__(self):
        if self.clients is None:
            self.clients = {}

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(WebSocketManager, cls).__new__(cls, *args, **kwargs)
        return cls.instance

    async def connect(self, user_id: int, websocket: WebSocket):
        self.clients[user_id] = websocket

    async def disconnect(self, user_id: int):
        self.clients.pop(user_id)

    async def broadcast(self, response: dict):
        for client in self.clients.values():
            if client is not None:
                await client.send_json(response)

    async def send_message(self, user_id: int, response: dict):
        websocket = self.clients[user_id]
        if websocket is None:
            return
        await websocket.send_json(response)
