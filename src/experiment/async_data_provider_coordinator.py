import socket
import select
import pickle

#from data_providers.metoffice import WeatherData

#pipe1 = WeatherData(0, 0, 0, 0, "", "")
socket1 = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
socket1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socket1.bind(('127.0.0.1', 5001))
socket1.listen(1)

socket2 = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
socket2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socket2.bind(('127.0.0.1', 5002))
socket2.listen(1)

sockets = [socket1, socket2]

pipe1 = None
pipe2 = None

while True:
    ports, _, _ = select.select(sockets, [], [], 1)
    for port in ports:
        if port is socket1:
            clientsocket, _ = port.accept()
            pipe1 = clientsocket
            sockets.append(clientsocket)
            print(f"Socket 1 Connected to {port}")
        elif port is socket2:
            clientsocket, _ = port.accept()
            pipe2 = clientsocket
            sockets.append(clientsocket)
            print(f"Socket 2 Connected to {port}")
        else:
            data = port.recv(2024)

            if not data:
                print(f"Lost cantact with {port}")
                sockets.remove(port)
            elif port is pipe1:
                print(f"Received string from pipe1: {data}")
            elif port is pipe2:
                weather = pickle.loads(data)
                print(f"Received weather: {weather}")
            else:
                print(f"Received string from unknown: {data}")

