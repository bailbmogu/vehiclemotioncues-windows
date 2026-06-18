import asyncio
import websockets

async def test_client():
    uri = "ws://127.0.0.1:8765"
    async with websockets.connect(uri) as websocket:
        await websocket.send('{"ax": 0, "ay": 0}')
        print("Successfully sent test data!")

asyncio.run(test_client())