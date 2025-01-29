import asyncio
import websockets
import os

# Dictionary to store registered clients
registered_clients = {}

# Set to store connected clients
connected_clients = set()

async def handle_client(websocket, path):
    
    # add to the client list
    connected_clients.add(websocket)

    try:
        async for message in websocket:
            print(f"Received: {message}")

            # Handle registration
            if message.startswith("REGISTER:"):
                client_id = message.split(":", 1)[1].strip()

                if client_id in registered_clients:
                    print('client already exists.')
                
                # Register the client
                registered_clients[client_id] = websocket
                await websocket.send(f"SUCCESS: Client '{client_id}' registered.")
                print(f"Client registered: {client_id}")

            # Handle file list request
            elif message == "file list":
                try:
                    files = os.listdir(".")  # Get list of files in the current directory
                    files_list = "\n".join(files)
                    await websocket.send(f"FILES:\n{files_list}")  # Send file names to the client
                    print("Sent list of files to client.")
                except Exception as e:
                    await websocket.send(f"ERROR: Unable to list files. {str(e)}")
            else:
                print(f'Unknown message: {message}')
    except websockets.ConnectionClosed:
        print("Client disconnected.")
    finally:
        # Remove the client from the set when disconnected
        connected_clients.remove(websocket)

        print(f"Client removed. Total clients: {len(connected_clients)}")
# Start the WebSocket server
async def main():
    async with websockets.serve(handle_client, "localhost", 8888):
        print("WebSocket server running on ws://localhost:8888")
        await asyncio.Future()  # Run forever

# Run the server
if __name__ == "__main__":
    asyncio.run(main())
