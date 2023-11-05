import socket
import threading
import time

def handle_client(client_socket):
    while True:
        try:
            current_time = custom_time()
            client_socket.send(current_time.encode())
            client_time = client_socket.recv(1024).decode()
            print(f"Cliente {client_socket.getpeername()} - Tempo registrado: {client_time}")
            time.sleep(1)
        except (ConnectionAbortedError, ConnectionResetError):
            print(f"Cliente {client_socket.getpeername()} encerrou a conexão.")
            break

def custom_time():
    global server_seconds
    server_seconds += 1
    server_seconds %= 86400 
    hours = server_seconds // 3600
    minutes = (server_seconds % 3600) // 60
    seconds = server_seconds % 60
    time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    print(f"Relógio do servidor: {time_str}")
    return time_str

def calculate_average_time():
    all_client_times = [convert_time_to_seconds(client_socket.recv(1024).decode()) for client_socket in clients]
    all_client_times.append(server_seconds) 
    average_time = sum(all_client_times) // len(all_client_times)
    return average_time

def convert_time_to_seconds(time_str):
    hours, minutes, seconds = map(int, time_str.split(":"))
    return hours * 3600 + minutes * 60 + seconds


def send_adjustments_to_clients():
    global server_seconds 
    while True:
        time.sleep(15)
        average_time = calculate_average_time()
        adjustment_seconds = average_time - server_seconds
        server_seconds += adjustment_seconds
        for client_socket in clients:
            client_time_seconds = convert_time_to_seconds(client_socket.recv(1024).decode())
            client_adjustment_seconds = average_time - client_time_seconds
            client_socket.send(f"ADJUST {client_adjustment_seconds}".encode())
            print(f"Instrução de ajuste enviada para o cliente {client_socket.getpeername()}.")
        print(f"Instrução de ajuste enviada para todos os clientes.")
        print(f"Relógio do servidor ajustado em {adjustment_seconds} segundos.")

HOST = '0.0.0.0' 
PORT = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

print(f"Servidor escutando em {HOST}:{PORT}")

server_seconds = 41400
clients = [] 

adjustment_thread = threading.Thread(target=send_adjustments_to_clients)
adjustment_thread.start()

while True:
    client, addr = server.accept()
    print(f"Conexão recebida de {addr[0]}:{addr[1]}")
    clients.append(client)

    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()