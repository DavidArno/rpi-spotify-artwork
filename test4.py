import compatibility
from i75_display_driver.spotify_view.spotify_broker import SpotifyBroker # type: ignore

try:
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
        print(1)
        test_view = DigitTestBroker(led_matrix.create_display())
        spotify_view = SpotifyBroker(led_matrix.create_display())
        print(2)
        broker_set = MessageBrokers(
            {
                message_headers.TEST_DIGIT: test_view.handle_digit_test_message,
                message_headers.SAVE_AND_DISPLAY_ARTWORK: spotify_view.handle_save_and_display_artwork
            }
        )
        print(3)
        handle_messages(lambda: stdin.read(1), print, broker_set)
        print(4)
    except Exception as e:
        print(f"Exception: {e}")
        led_matrix._hub.set_rgb(2, 2, 255, 0, 0)
        led_matrix._hub.set_rgb(2, 3, 255, 0, 0)
        led_matrix._hub.set_rgb(3, 2, 255, 0, 0)
        led_matrix._hub.set_rgb(3, 3, 255, 0, 0)
        led_matrix._hub.flip()
        raise

except Exception as e:
    print(f"Died with exception:{e}\r\n{e.value}") # type: ignore

