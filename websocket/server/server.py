import asyncio
import websockets

# Handle WebSocket connections and messages
async def echo(websocket, path):
    async for message in websocket:
        print(f"Received: {message}")
        # Echo the received message back to the client
        await websocket.send(f"Echo: {message}")

# Start the WebSocket server
async def main():
    async with websockets.serve(echo, "localhost", 8765):
        print("WebSocket server running on ws://localhost:8765")
        await asyncio.Future()  # Run forever

# Run the server
if __name__ == "__main__":
    asyncio.run(main())
