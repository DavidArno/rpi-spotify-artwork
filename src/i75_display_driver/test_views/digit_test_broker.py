################################################################################
# This is a simple test message broker that expects a single digit character
# as the message body and it draws it in white on a 0x400000 background on the 
# lcd matrix
################################################################################
from hub75_display.colours import rgb_colour_to_hub75_colour
from hub75_display.display import Display, Layer
from i75_display_driver.shared.numbers import get_coloured_digit_image_data
from rpi_spotify_shared.message_handler.message_types import MessageBody
from third_party.decoder_types import RGBColour


class DigitTestBroker():
    def __init__(self, display:Display):
        self._display = display

    def handle_digit_test_message(self, digit:MessageBody) -> bool:
        sprite = get_coloured_digit_image_data(
            int(digit),
            rgb_colour_to_hub75_colour(RGBColour(0x400000)), 
            rgb_colour_to_hub75_colour(RGBColour(0xFFFFFF))
        )
        
        self._display.draw_sprite(2, 2, sprite, layer = Layer.Bottom)
        self._display.render_display()
        return True
        