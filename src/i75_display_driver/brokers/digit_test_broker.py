################################################################################
# This is a simple test message broker that expects a single digit character
# as the message body and it draws it in white on the lcd matrix
################################################################################

# type: ignore
from i75_display_driver.graphics.colours import packed_rgb_to_rgb
from i75_display_driver.graphics.numbers import get_coloured_digit_image_data


class DigitTestBroker():
    def __init__(self, hub75matrix):
        self._hub = hub75matrix

    def handle_digit_test_message(self, digit):
        digit = get_coloured_digit_image_data(int(digit), 0x400000, 0xFFFFFF)
        for x in range(5):
            for y in range(9):
                (r, g, b) = packed_rgb_to_rgb(digit[x][y])
                self._hub.set_rgb(x+2, y+2, r, g, b)
        
        self._hub.flip()