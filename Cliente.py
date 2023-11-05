import socket
import time
import threading
import random

def custom_time():
    global client_seconds
    client_seconds += 1
    client_seconds %= 86400 
    hours = client_seconds // 3600
    minutes = (client_seconds % 3600) // 60
    seconds = client_seconds % 60
    time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return time_str

def handle_instructions():
    while True:
        instruction = client.recv(1024).decode()
        if instruction.startswith("ADJUST"):
            _, adjustment_seconds = instruction.split()
            adjustment_seconds = int(adjustment_seconds)
            adjust_clock(adjustment_seconds)
            print(f"Relógio do cliente ajustado em {adjustment_seconds} segundos.")
        time.sleep(1)

def adjust_clock(adjustment_seconds):
    global client_seconds
    client_seconds += adjustment_seconds
    client_seconds %= 86400 

def initialize_random_clock():
    global client_seconds
    client_seconds = random.randint(3600, 86400) 
    print(f"Relógio do cliente inicializado com {client_seconds} segundos")

HOST = 'localhost'
PORT = 8080

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

initialize_random_clock()

instruction_handler = threading.Thread(target=handle_instructions)
instruction_handler.start()

while True:
    current_time = custom_time()
    client.send(current_time.encode())
    time.sleep(1)
