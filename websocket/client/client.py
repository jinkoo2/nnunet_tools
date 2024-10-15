import asyncio
import websockets

async def hello():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        # Send a message to the server
        await websocket.send("Hello, Server!")
        print("Sent: Hello, Server!")

        # Receive a response from the server
        response = await websocket.recv()
        print(f"Received: {response}")

# Run the client
if __name__ == "__main__":
    asyncio.run(hello())
