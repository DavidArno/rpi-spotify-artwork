from hub75_display.display import Display, Layer
from hub75_display.sprites import create_sprite_from_jpeg_data
from rpi_spotify_shared.message_handler.message_types import MessageBody
from rpi_spotify_shared.message_handler.spotify_artwork_messages import \
    convert_message_body_to_file_data, \
    convert_message_body_to_progress

from hub75_display.colours import Hub75Colour, rgb_values_to_hub75_colour

_BLACK:Hub75Colour = rgb_values_to_hub75_colour(0, 0, 0) # type: ignore
_DARK_GREY:Hub75Colour = rgb_values_to_hub75_colour(64, 64, 64) # type: ignore
_MID_GREY:Hub75Colour = rgb_values_to_hub75_colour(128, 128, 128) # type: ignore
_LIGHT_GREY:Hub75Colour = rgb_values_to_hub75_colour(192, 192, 192) # type: ignore
_PROGRESS_ILLUMINATED:Hub75Colour = rgb_values_to_hub75_colour(141, 98, 178) # type: ignore

class SpotifyBroker:
    def __init__(self, display:Display):
        self._display = display

    def handle_save_and_display_artwork(self, message:MessageBody) -> bool:
        _, jpeg_data = convert_message_body_to_file_data(message)
        sprite = create_sprite_from_jpeg_data(jpeg_data)
        self._display.draw_sprite(0, 0, sprite, layer = Layer.Bottom)
        self._resume()
        self._draw_progress_container()
        self._display.render_display()
        return True

    def handle_progress(self, message:MessageBody) -> bool:
        so_far_time, total_time = convert_message_body_to_progress(message)
        width = int(so_far_time / total_time * 50)

        if width > 0:
            self._display.flood_fill(7, 55, width, 3, _PROGRESS_ILLUMINATED, layer = Layer.Top)

        if width < 50:
            self._display.flood_fill(8 + width, 55, 50 - width, 3, _BLACK, layer = Layer.Top)

        self._display.render_display()
        return True

    def handle_pause(self, _:str) -> bool:
        self._pause()
        self._display.render_display()
        return True

    def handle_resume(self, _:str) -> bool:
        self._resume()
        self._display.render_display()        
        return True
        
    def _draw_progress_container(self) -> None:
        self._draw_indented_rectangle(Layer.Top, 6, 54, 52, 5)

    def _pause(self):
        self._draw_indented_rectangle(Layer.Top, 22, 11, 7, 32)
        self._draw_indented_rectangle(Layer.Top, 35, 11, 7, 32)

    def _resume(self):
        self._flood_fill(Layer.Top, 22, 11, 7, 32, _BLACK)
        self._flood_fill(Layer.Top, 35, 11, 7, 32, _BLACK)

    def _draw_indented_rectangle(self, layer:Layer, x:int, y:int, width:int, height:int):
        self._display.draw_horizontal_line(x, y, width-1, _DARK_GREY, layer=layer)
        self._display.draw_vertical_line(x, y+1, height-2, _DARK_GREY, layer=layer)
        self._display.draw_horizontal_line(x+1, y + height - 1, width-1, _LIGHT_GREY, layer=layer)
        self._display.draw_vertical_line(x + width - 1, y+1, height-2, _LIGHT_GREY, layer=layer)
        self._display.set_pixel(x + width - 1, y, _MID_GREY, layer=layer)
        self._display.set_pixel(x, y + height - 1, _MID_GREY, layer=layer)
        self._display.flood_fill(x+1, y+1, width-2, height-2, _MID_GREY, layer=layer)

