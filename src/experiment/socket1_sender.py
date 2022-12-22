import socket
import pickle

from data_providers.metoffice import WeatherData

weather = pickle.dumps(WeatherData(1, 2, 3, 4, "foo", "bar"))

socket1 = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
socket1.connect(('127.0.0.1', 5001))

socket2 = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
socket2.connect(('127.0.0.1', 5002))

socket1.send(b"1Hello")
socket2.send(weather)
socket1.close()
socket1 = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
socket1.connect(('127.0.0.1', 5001))

socket1.send(b"2Hello again")
socket1.close()
socket1 = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
socket1.connect(('127.0.0.1', 5001))

socket1.send(b"3Goodbye")
socket1.close()

