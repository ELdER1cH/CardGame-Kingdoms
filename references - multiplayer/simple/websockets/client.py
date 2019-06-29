#!/usr/bin/env python

# WSS (WS over TLS) client example, with a self-signed certificate

import asyncio
#import pathlib
#import ssl
import websockets

#ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
#ssl_context.load_verify_locations(
#    pathlib.Path(__file__).with_name('localhost.pem'))

async def hello():
    async with websockets.connect(
        #'wss://localhost:8765', ssl=ssl_context) as websocket:
            'ws://192.168.2.153:8765') as websocket:
        #name = input("What's your name? ")

        #await websocket.send(name)
        #print(f"> {name}")
        async for message in websocket:
            print(f"< {message}")

#async def consumer_handler(websocket, path):
#    async for message in websocket:
#        await consumer(message)        
        #while True:
        #  greeting = await websocket.recv()
        #  print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())
