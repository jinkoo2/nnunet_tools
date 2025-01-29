import asyncio
import websockets

async def handle_messages(websocket):
    """Continuously listen for messages from the server."""
    try:
        async for message in websocket:
            print(f"Received from server: {message}")
    except websockets.ConnectionClosed:
        print("Connection closed by the server.")

async def send_messages(websocket):
    """Continuously send messages to the server."""
    try:
        while True:
            message = input("Enter a message to send to the server (or 'quit' to exit): ")
            if message.lower() == "quit":
                print("Closing connection...")
                break
            await websocket.send(message)
            print(f"Sent: {message}")
    except websockets.ConnectionClosed:
        print("Connection closed by the server.")

async def connect_and_run():
    uri = "ws://localhost:8888"
    client_id = "client_1"  # Unique ID for this client

    while True:  # Reconnection loop
        try:
            print(f"Attempting to connect to {uri}...")
            async with websockets.connect(uri) as websocket:
                print("Connected to server.")
                
                # Register the client
                await websocket.send(f"REGISTER:{client_id}")
                response = await websocket.recv()
                print(f"Registration Response: {response}")

                # If registration is successful, start communication
                if "SUCCESS" in response:
                    # Run tasks for sending and receiving messages concurrently
                    listener_task = asyncio.create_task(handle_messages(websocket))
                    sender_task = asyncio.create_task(send_messages(websocket))

                    # Wait for both tasks to complete
                    await asyncio.gather(listener_task, sender_task)
                else:
                    print(f"Failed to register: {response}")
                    break

        except (websockets.ConnectionClosed, ConnectionRefusedError):
            print("Connection lost. Retrying in 5 seconds...")
            await asyncio.sleep(5)  # Wait before retrying
        except Exception as e:
            print(f"An error occurred: {e}. Retrying in 5 seconds...")
            await asyncio.sleep(5)

# Run the client
if __name__ == "__main__":
    asyncio.run(connect_and_run())
