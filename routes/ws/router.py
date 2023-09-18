import asyncio
from json.decoder import JSONDecodeError

from fastapi import APIRouter, WebSocket

# admin credentials simplified
USER = 'admin'
PASSWORD = 'admin'

ws_router = APIRouter(prefix='/ws')


@ws_router.websocket('/admin')
async def admin(ws: WebSocket):
    try:
        await ws.accept()
        in_message = await ws.receive_json()
        if in_message.get('user') != USER or in_message.get('password') != PASSWORD:
            print(f'INFO: invalid credentials received from ws client: {ws.client}')
            await ws.send_json({'message': 'failed to login'})
            await ws.close()
            return

        while True:
            # ordered_book = await get_ordered_book()
            await ws.send_json({'message': 'hello'})

            print(ws.client)
            await asyncio.sleep(2)
            
            
    except JSONDecodeError:
        print(f'ERROR: unsupported message format received from ws client: {ws.client}')
        await ws.close(code=1007)
    except Exception as e:
        print(f'ERROR: {e}')
        await ws.close(code=1011)
