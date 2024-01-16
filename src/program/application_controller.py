import os
import socket
import time
from typing import Any, cast

from controllers.mandelbrot_controller import MandelbrotController
from controllers.space_invaders_controller import SpaceInvadersController
from controllers.spotify_controller import SpotifyController
from controllers.weather_forecast_controller import WeatherForecastController
from controllers.wot_no_spotify_controller import WotNoSpotifyController
from data_providers.mandelbrot import MandelbrotSet
from data_providers.metoffice import MetOffice
from data_providers.spotify_currently_playing import SpotifyCurrentlyPlaying
from common.graphics.canvas import Canvas, Layer
from common.graphics.colours import GREEN, RED, WHITE, RGBColour
from rpi_spotify_shared import matrix_details, socket_details

raw_metoffice_key = os.environ.get('DATAPOINT_API_KEY')
if raw_metoffice_key is None:
    raise RuntimeError("DATAPOINT_API_KEY environment variable is not defined")
else:
    met_office_key = str(raw_metoffice_key)

met_office =  MetOffice(met_office_key)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((socket_details.HOST, socket_details.PORT))


def render_frame_count(canvas_ref:Any) -> None:
    global last_frame_count
    canvas = cast(Canvas, canvas_ref)
    canvas.flood_fill(0, 61, 22, 3, RGBColour(0x010101), layer = Layer.Debug)
    canvas.set_pixel(1, 62, WHITE, layer = Layer.Debug)
    canvas.set_pixel(22, 62, WHITE, layer = Layer.Debug)
    canvas.draw_horizontal_line(2, 62, last_frame_count, GREEN, layer = Layer.Debug)
    canvas.draw_horizontal_line(2 + last_frame_count, 62, 20 - last_frame_count, RED, layer = Layer.Debug)


spotify_canvas = Canvas(matrix_details.DISPLAY_WIDTH, matrix_details.DISPLAY_HEIGHT, render_frame_count)
wot_no_canvas = Canvas(matrix_details.DISPLAY_WIDTH, matrix_details.DISPLAY_HEIGHT, render_frame_count)
mandelbrot_canvas = Canvas(matrix_details.DISPLAY_WIDTH, matrix_details.DISPLAY_HEIGHT, render_frame_count)
weather_canvas = Canvas(matrix_details.DISPLAY_WIDTH, matrix_details.DISPLAY_HEIGHT, render_frame_count)
invader_canvas = Canvas(matrix_details.DISPLAY_WIDTH, matrix_details.DISPLAY_HEIGHT, render_frame_count)

spotify_controller = SpotifyController(spotify_canvas, SpotifyCurrentlyPlaying())
wot_no_controller = WotNoSpotifyController(wot_no_canvas, lambda: True)
weather_controller = WeatherForecastController(weather_canvas, met_office, lambda: True)
mandelbrot_controller = MandelbrotController(mandelbrot_canvas, MandelbrotSet(64, 64), lambda: False)
invader_controller = SpaceInvadersController(invader_canvas, lambda: True)

frame_count = 0
last_frame_count = 0
seconds_count = time.time()

while True:
    start_time = time.time()
    if spotify_controller.actively_displaying(start_time):
        data = spotify_canvas.render_as_bytes()
    elif weather_controller.actively_displaying(start_time):
        data = weather_canvas.render_as_bytes()
    elif mandelbrot_controller.actively_displaying(start_time):
        data = mandelbrot_canvas.render_as_bytes()
    elif invader_controller.actively_displaying(start_time):
        data = invader_canvas.render_as_bytes()
    else:
        data  = wot_no_canvas.render_as_bytes()

    sock.send(data)
    end_time = time.time()
    frame_count += 1
    delay = 0.05 - (end_time - start_time)
    if delay > 0:
        time.sleep(delay)

    if end_time - seconds_count > 1:
        last_frame_count = frame_count
        frame_count = 0
        seconds_count = end_time

