import shim_setup # type: ignore

from hub75_display.led_matrix import LedMatrix
from i75_display_driver.test_views.digit_test_broker import DigitTestBroker
from rpi_spotify_shared.message_handler import message_headers
from rpi_spotify_shared.message_handler.message_state_machine import handle_messages
from rpi_spotify_shared.message_handler.message_types import MessageBrokers
from sys import stdin

led_matrix = LedMatrix(64, 64, stb_invert=True)
led_matrix._hub.set_rgb(2, 2, 0, 255, 0)
led_matrix._hub.flip()

try:
    test_view = DigitTestBroker(led_matrix.create_display())
    broker_set = MessageBrokers(
        {
            message_headers.TEST_DIGIT: test_view.handle_digit_test_message
        }
    )

    handle_messages(lambda: stdin.read(1), print, broker_set)
except:
    led_matrix._hub.set_rgb(2, 2, 255, 0, 0)
    led_matrix._hub.set_rgb(2, 3, 255, 0, 0)
    led_matrix._hub.set_rgb(3, 2, 255, 0, 0)
    led_matrix._hub.set_rgb(3, 3, 255, 0, 0)
    led_matrix._hub.flip()

