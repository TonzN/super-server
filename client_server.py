import socket
import asyncio
import json
import time
import client_manager as manager

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 12345  # The port used by the server

config_path = "config.json" #incase path changes
users_path = "users.json" #incase path changes
run_terminal = True
short_lived_client = True

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


user_capacity = config["user_capacity"]
client_cmds = config["client_cmds"]

def send_to_server(client_sock, msg):
    try:
        client_sock.sendall(msg)
    except Exception as e:
        print(f"Could not send message to server {e}\n")

def recieve_from_server(client_sock):
    try:
        data = client_sock.recv(1024)
    except Exception as e:
        print(f"Could not recieve from server: {e}\n")
        return
    return data.decode()

def new_user_protocol():
    pass

def client_joined(client_sock):
    user = input("Username: ")
    existing_user = False
    send_to_server(client_sock, ("verify_user", user))

def client(): #activates a client
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_sock:
        client_sock.setblocking(False)
        try:
            client_sock.connect(HOST, PORT)
            print(f"Client {id} connected.\n")
        except Exception as e:
            print(f"Client {id} did not connect: {e}\n")


        if not short_lived_client:
            client_inp = input("Input to server: ")
            print("\n")
        else:
            try:
                client_sock.sendall(str(id).encode())
            except Exception as e:
                print(f"Could not send message to server {e}\n")
            
            try:
                data = client_sock.recv(1024)
                print(data.decode())
            except Exception as e:
                print(f"Could not recieve from server: {e}\n")
  
            client_sock.close()
            print(f"Disconnected client {id}\n")
    
def main():
    cmd = input("command: ")
    if cmd == "close":
        run_terminal = False
        return

    client()

while run_terminal:
    time.sleep(0.1)
    main()