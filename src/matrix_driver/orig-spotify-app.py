import time
import sys
import requests

from io import BytesIO
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw

def setup_matrix():
    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 64
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = 'adafruit-hat'
    options.brightness = 100
    options.gpio_slowdown = 4
    return RGBMatrix(options = options)


current_image = ""
current_bar_width = 0


base_no_spotify_image = 0

# fill = (28, 28, 28)
# draw.rectangle((4, 57, 20, 59), fill=(30, 30, 200), outline=(30, 30, 200))

# Configuration for the matrix

#matrix.SetImage(image.convert('RGB'))


###

current_duration = 123906
current_progress_increment = 7000
current_progress = 0
###


def main_loop():
    second_counter = 0
    first_pass = True

    try:
        print("Press CTRL-C to stop.")

        while True:
            time.sleep(0.2)
            second_counter += 1
            if second_counter == 5 or first_pass:
                first_pass = False
                second_counter = 0
                (spotify_running, album_image_url, elapsed_time, track_length, paused) = spotify_current_playing(0)

                if spotify_running:
                    refresh_spotify_display(album_image_url, elapsed_time, track_length, paused)
                else:
                    refresh_sleep_display()

    except KeyboardInterrupt:
        sys.exit(0)

def spotify_current_playing(sp):
    print("spotify_current_playing")
    global current_progress
    global current_progress_increment

    current_progress += current_progress_increment
    if current_progress > current_duration:
        return (False, "", 0, 0, False)
    else:
        return (
            True, 
            "https://i.scdn.co/image/ab67616d00004851cafe9404f872e4c0e91a8cc8", 
            current_progress, 
            current_duration, 
            False
            )

def refresh_spotify_display(album_image_url, elapsed_time, track_length, paused):
    refresh_image = False

    global base_spotify_image
    global progress_spotify_image
    global paused_spotify_image
    global current_bar_width

    if album_image_url != current_album_image_url:
        response = requests.get("https://i.scdn.co/image/ab67616d00004851cafe9404f872e4c0e91a8cc8")
        base_spotify_image = Image.open(BytesIO(response.content))
        
        progress_spotify_image = base_spotify_image.copy()
        draw_progress_container(progress_spotify_image)

        paused_spotify_image = base_spotify_image.copy()
        refresh_image = True

    bar_width = int(elapsed_time / track_length * 55)
    if bar_width > current_bar_width:
        current_bar_width = bar_width
        draw_progress_bar(progress_spotify_image, current_bar_width)
        refresh_image = True

    if refresh_image:
        print("refresh_spotify_display {}/{}".format(elapsed_time, track_length))
        matrix.SetImage(progress_spotify_image.convert('RGB'))


def refresh_sleep_display():
    global base_no_spotify_image

    if base_no_spotify_image == 0:
        print("refresh_sleep_display")
        base_no_spotify_image = Image.open("./wot-no-spotify.png")
        matrix.SetImage(base_no_spotify_image.convert('RGB'))

main_loop()