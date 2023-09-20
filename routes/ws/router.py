from json.decoder import JSONDecodeError

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder

from utils.constants import Book

# admin credentials simplified
USER = 'admin'
PASSWORD = 'admin'

ws_router = APIRouter(prefix='/ws')


class ConnectionManager:
    def __init__(self):
        self.connections = []

    async def connect_with_credentials_or_fail(self, ws: WebSocket) -> None:
        try:
            await ws.accept()
            message = await ws.receive_json()
            if message.get('user') != USER or message.get('password') != PASSWORD:
                print(f'INFO: invalid credentials received from ws client: {ws.client}')
                await ws.send_json({'message': 'failed to login due to invalid credentials'})
                await ws.close()
                return

            await ws.send_json({'message': 'successfully logged in'})
            self.connections.append(ws)
        except JSONDecodeError:
            print(f'ERROR: unsupported message format received from ws client: {ws.client}')
            await ws.close(code=1007)
        except Exception as e:
            print(f'ERROR: {e}')
            await ws.close(code=1011)

    async def broadcast_book_order_to_admins(self, book: Book) -> None:
        for ws in self.connections:
            await ws.send_json({
                'message': 'book order placed',
                'book': jsonable_encoder(book),
            })

    async def disconnect_all_clients(self) -> None:
        for ws in self.connections:
            await ws.close()
        self.connections.clear()

    def remove_ws_client_from_connections(self, ws: WebSocket) -> None:
        self.connections.remove(ws)


admin_connection_manager = ConnectionManager()


@ws_router.websocket('/admin')
async def admin(ws: WebSocket):
    await admin_connection_manager.connect_with_credentials_or_fail(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        admin_connection_manager.remove_ws_client_from_connections(ws)
        print(f'INFO: ws client disconnected: {ws.client}')
