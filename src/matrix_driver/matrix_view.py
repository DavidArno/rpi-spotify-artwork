from typing import Any
from rgbmatrix import RGBMatrix, RGBMatrixOptions #type: ignore
from PIL import Image #type: ignore
from rpi_spotify_shared import matrix_details, socket_details
import socket

options:Any = RGBMatrixOptions()
options.rows = matrix_details.DISPLAY_WIDTH
options.cols = matrix_details.DISPLAY_HEIGHT
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'
options.gpio_slowdown = 5

matrix:Any = RGBMatrix(options = options)
image = Image.new('RGB', (64, 64))

canvas_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
canvas_socket.bind((socket_details.HOST, socket_details.PORT))
canvas_socket.listen(1)
connection, _ = canvas_socket.accept()

while True:
    data = connection.recv(matrix_details.RAW_IMAGE_BYTES)
    if len(data) == 0: break

    image.frombytes(data) #type: ignore
    matrix.SetImage(image)