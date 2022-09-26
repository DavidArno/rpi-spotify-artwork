import sys
print(f"version = {sys.version}")
import shim_setup # type: ignore
print("shim setup")

try:
    print("SomeType")
    SomeType = object
    x:SomeTYpe = 1
except Exception as e:
    print(f"Sometype Error: {e}")

try:
    from hub75_display.led_matrix import LedMatrix
except Exception as e:
    print(f"hub75 Error: {e}")
try:
    from i75_display_driver.test_views.digit_test_broker import DigitTestBroker
except Exception as e:
    print(f"i75 Error: {e}")
try:
    from rpi_spotify_shared.message_handler import message_headers
except Exception as e:
	print(f"shared Error: {e}")
try:
    from rpi_spotify_shared.message_handler.message_state_machine import handle_messages
except Exception as e:
	print(f"shared 2 Error: {e}")
try:
    from rpi_spotify_shared.message_handler.message_types import MessageBrokers
except Exception as e:
	print(f"shared 3 Error: {e}")

try:
    def test() -> 'list[int]':
        row:'list[int]' = [1,2,3]
        return row

    if (y := test()) and y[0] == 1:
        print(":= works")
except Exception as e:
    print(f":= Error: {e}")

try:
    FilePath = str
    XYP = 'tuple[int, int, int]'
    PixelRenderer = callable
    print("types work")
except Exception as e:
    print(f"XYP Error: {e}")
#from sys import stdin
#
#led_matrix = LedMatrix(64, 64, stb_invert=True)
#led_matrix._hub.set_rgb(2, 2, 0, 255, 0)
#led_matrix._hub.flip()
#
#try:
#    test_view = DigitTestBroker(led_matrix.create_display())
#    broker_set = MessageBrokers(
#        {
#            message_headers.TEST_DIGIT: test_view.handle_digit_test_message
#        }
#    )
#
#    handle_messages(lambda: stdin.read(1), print, broker_set)
#except:
#    led_matrix._hub.set_rgb(2, 2, 255, 0, 0)
#    led_matrix._hub.set_rgb(2, 3, 255, 0, 0)
#    led_matrix._hub.set_rgb(3, 2, 255, 0, 0)
#    led_matrix._hub.set_rgb(3, 3, 255, 0, 0)
#    led_matrix._hub.flip()


