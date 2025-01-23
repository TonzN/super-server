import socket
import threading
import asyncio
import json
import subprocess

config_path = "config.json" #incase path changes
users_path = "users.json"

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

try: #attempt fetching users
    with open(config_path, 'r') as file:
        users = json.load(file)
        print("JSON file loaded successfully!")
except FileNotFoundError:
    print(f"Error: The file '{users_path}' does not exist.")
except json.JSONDecodeError:
    print(f"Error: The file '{users_path}' contains invalid JSON.")
except PermissionError:
    print(f"Error: Permission denied while accessing '{users_path}'.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")


HOST = config["HOST"]
PORT = config["PORT"]
client_capacity = config["user_capacity"]
func_keys = config["function_keys"]

async def update_users_count():
    config["user_count"] += 1

def verify_user(username):
    if username in users:
        return 1
    else:
        return -1

async def client_handler(client_socket):
    loop = asyncio.get_event_loop()
    try:
        data = await loop.sock_recv(client_socket, 1024) #first 4 letters are function keywords
        data = data.decode()
        function = data[0:4]
        if function in func_keys: 
            try:
                reponse = str(globals()[func_keys[function]](data)) 
            except Exception as e:
                reponse = None
                print(f"Function is not a valid server request: {e}")

        if reponse:
            await loop.sock_sendall(client_socket, reponse.encode())
    
    except Exception as e:
        print(f"could not recieve or send back to client {e}")
    
    finally:
        client_socket.close()

async def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(client_capacity)
        server_socket.setblocking(False)
        loop = asyncio.get_event_loop()
        print("Server spawned!!")

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


async def main():
    await run_server()

asyncio.run(main())
