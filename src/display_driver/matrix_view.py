from rgbmatrix import RGBMatrix, RGBMatrixOptions #type: ignore
from PIL import Image
from rpi_spotify_shared import matrix_details, socket_details
import socket

options = RGBMatrixOptions()
options.rows = matrix_details.DISPLAY_WIDTH
options.cols = matrix_details.DISPLAY_HEIGHT
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'
options.gpio_slowdown = 4

matrix = RGBMatrix(options = options)
image = Image.new('RGB', (64, 64))

view_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
view_socket.connect((socket_details.HOST, socket_details.PORT))

while True:
    data = view_socket.recv(matrix_details.RAW_IMAGE_BYTES)
    if len(data) == 0: break

    image.frombytes(data)
    matrix.SetImage(image)