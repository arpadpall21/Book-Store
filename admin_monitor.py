import asyncio
import websockets
import json

credentials = {
    'user': 'admin_',
    'password': 'admin_',
}


async def ws_client():
    async with websockets.connect('ws://localhost:3000/ws/admin') as websocket:
        await websocket.send(json.dumps(credentials))
        while True:
            print(await websocket.recv())

if __name__ == '__main__':
    asyncio.run(ws_client())
