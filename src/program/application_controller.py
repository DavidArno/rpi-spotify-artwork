import socket
import time
from views.view import View, Layer
from rpi_spotify_shared import matrix_details
from rpi_spotify_shared import socket_details
from views.numbers import get_coloured_digit_sprite
from views.colours import BLACK, WHITE
from data_providers.spotify_currently_playing import SpotifyCurrentlyPlaying
from controllers.spotify.spotify_controller import SpotifyController


view = View(matrix_details.DISPLAY_WIDTH, matrix_details.DISPLAY_HEIGHT)
spotify = SpotifyCurrentlyPlaying()
spotify_controller = SpotifyController(view, spotify)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((socket_details.HOST, socket_details.PORT))

while True:
        spotify_controller.actively_displaying(time.time())
        data = view.render_as_bytes()
        sock.send(data)
        time.sleep(0.05)
        print("tick")

