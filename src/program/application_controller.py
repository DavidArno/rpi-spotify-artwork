import socket
import time
import os

from data_providers.mandelbrot import MandelbrotSet
from controllers.mandelbrot_controller import MandelbrotController
from data_providers.metoffice import MetOffice
from graphics.canvas import Canvas
from rpi_spotify_shared import matrix_details
from rpi_spotify_shared import socket_details
from data_providers.spotify_currently_playing import SpotifyCurrentlyPlaying
from controllers.spotify_controller import SpotifyController
from controllers.weather_forecast_controller import WeatherForecastController

spotify_canvas = Canvas(matrix_details.DISPLAY_WIDTH, matrix_details.DISPLAY_HEIGHT)
wot_no_canvas = Canvas(matrix_details.DISPLAY_WIDTH, matrix_details.DISPLAY_HEIGHT)
spotify = SpotifyCurrentlyPlaying()
spotify_controller = SpotifyController(spotify_canvas, spotify)
met_office =  MetOffice(os.environ.get('DATAPOINT_API_KEY'))

wot_no_controller = WeatherForecastController(wot_no_canvas, met_office, lambda: True) 
#wot_no_controller = MandelbrotController(wot_no_canvas, MandelbrotSet(64, 64), lambda: True)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((socket_details.HOST, socket_details.PORT))

while True:
    if spotify_controller.actively_displaying(time.time()):
        data = spotify_canvas.render_as_bytes()
    else:
        wot_no_controller.actively_displaying(time.time())
        data  = wot_no_canvas.render_as_bytes()
    
    sock.send(data)
    time.sleep(0.1)

