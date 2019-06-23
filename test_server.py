import asyncio
import json
import logging
import websockets
from logging import getLogger, INFO, StreamHandler

logger = getLogger('websockets')
logger.setLevel(INFO)
logger.addHandler(StreamHandler())

async def counter(websocket, path):
    async for message in websocket:
      data = json.loads(message)
      print(data)
        
asyncio.get_event_loop().run_until_complete(
    websockets.serve(counter, 'localhost', 8765))
asyncio.get_event_loop().run_forever()
