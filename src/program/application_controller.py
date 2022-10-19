import os
import socket
import time

from controllers.mandelbrot_controller import MandelbrotController
from controllers.space_invaders_controller import SpaceInvadersController
from controllers.spotify_controller import SpotifyController
from controllers.weather_forecast_controller import WeatherForecastController
from controllers.wot_no_spotify_controller import WotNoSpotifyController
from data_providers.mandelbrot import MandelbrotSet
from data_providers.metoffice import MetOffice
from data_providers.spotify_currently_playing import SpotifyCurrentlyPlaying
from graphics.canvas import Canvas
from rpi_spotify_shared import matrix_details, socket_details

raw_metoffice_key = os.environ.get('DATAPOINT_API_KEY')
if raw_metoffice_key is None:
    raise RuntimeError("DATAPOINT_API_KEY environment variable is not defined")
else:
    met_office_key = str(raw_metoffice_key)

met_office =  MetOffice(met_office_key)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((socket_details.HOST, socket_details.PORT))

spotify_canvas = Canvas(matrix_details.DISPLAY_WIDTH, matrix_details.DISPLAY_HEIGHT)
wot_no_canvas = Canvas(matrix_details.DISPLAY_WIDTH, matrix_details.DISPLAY_HEIGHT)
mandelbrot_canvas = Canvas(matrix_details.DISPLAY_WIDTH, matrix_details.DISPLAY_HEIGHT)
weather_canvas = Canvas(matrix_details.DISPLAY_WIDTH, matrix_details.DISPLAY_HEIGHT)
invader_canvas = Canvas(matrix_details.DISPLAY_WIDTH, matrix_details.DISPLAY_HEIGHT)

spotify_controller = SpotifyController(spotify_canvas, SpotifyCurrentlyPlaying())
wot_no_controller = WotNoSpotifyController(wot_no_canvas, lambda:True)
weather_controller = WeatherForecastController(wot_no_canvas, met_office, lambda: False) 
mandelbrot_controller = MandelbrotController(mandelbrot_canvas, MandelbrotSet(64, 64), lambda: True)
invader_controller = SpaceInvadersController(invader_canvas, lambda: True)

while True:
    now = time.time()
#    if spotify_controller.actively_displaying(now):
#        data = spotify_canvas.render_as_bytes()
    if weather_controller.actively_displaying(now):
        data = weather_canvas.render_as_bytes()
    elif mandelbrot_controller.actively_displaying(now):
        data = mandelbrot_canvas.render_as_bytes()
    elif invader_controller.actively_displaying(now):
        data = invader_canvas.render_as_bytes()
    else:
        data  = wot_no_canvas.render_as_bytes()

    sock.send(data)
#    time.sleep(0.1)