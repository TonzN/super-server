import socket
import threading
import asyncio
import json
import subprocess

config_path = "config.json" #incase path changes

#load paths
try: #attempt fetching configs
    with open(config_path, 'r') as file:
        config = json.load(file)
        print("JSON file loaded successfully!")
except FileNotFoundError:
    print(f"Error: The file '{config_path}' does not exist.")
except json.JSONDecodeError:
    print(f"Error: The file '{config_path}' contains invalid JSON.")
except PermissionError:
    print(f"Error: Permission denied while accessing '{config_path}'.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")


HOST = config["HOST"]
PORT = config["PORT"]

async def client_handler(client_socket):
    loop = asyncio.get_event_loop()
    try:
        data = await loop.sock_recv(client_socket, 1024)
        message = data.decode()
        message = f"Hello client {message}\n"
        await loop.sock_sendall(client_socket, message.encode())
    
    except Exception as e:
        print(f"could not recieve or send back to client {e}")
    
    finally:
        client_socket.close()

async def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        server_socket.setblocking(False)
        loop = asyncio.get_event_loop()

        while config["run_server"]:
            try: 
                client_socket, client_addr = await loop.sock_accept(server_socket)
                print(f"Accepted connection from {client_addr}")

                # Handle the client in a separate coroutine
        
                asyncio.create_task(client_handler(client_socket))
            except Exception as e:
                print("Error in main loop {e} \n")

    print("closing server\n")
    

async def main():
    await run_server()

asyncio.run(main())
