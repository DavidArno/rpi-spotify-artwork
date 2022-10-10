from typing import Callable
from graphics.beaufort import get_colour_for_speed
from graphics.colours import TIME_COLOUR, RGBColour, BLACK
from graphics.canvas import Canvas, Layer
from graphics.compass import get_coloured_compass_sprite
from graphics.sprites import Sprite, create_sprite_from_image
from data_providers.metoffice import MetOffice, WeatherData
from PIL import Image #type: ignore
from graphics.temperatures import get_colour_for_temperature

class WeatherForecastController():
    def __init__(self, canvas:Canvas, metoffice:MetOffice, check_enabled:Callable[[], bool]):
        self._canvas = canvas
        self._check_enabled = check_enabled
        self._draw_top_layer()
        self._draw_bottom_layer()
        self._last_time = 0.0
        self._metoffice = metoffice
        self._weather_symbol_sprites:dict[str, Sprite] = {}

    def actively_displaying(self, current_time:float) -> bool:
        if not self._check_enabled(): return False

        if current_time >= self._last_time + 3600.0:
            self._last_time = current_time
            self._draw_forecast(self._metoffice.get_forecast())

        self._canvas.draw_time(37, 2, TIME_COLOUR, current_time)
        return True

    def _draw_bottom_layer(self) -> None:
        self._draw_fixed_layer('bottom', Layer.Bottom)

    def _draw_top_layer(self) -> None:
        self._draw_fixed_layer('top', Layer.Top)

    def _draw_fixed_layer(self, image_id:str, layer:Layer) -> None:
        image = Image.open(f'images/weather/{image_id}_layer.png').convert('RGB')
        sprite = create_sprite_from_image(image)
        self._canvas.draw_sprite(0, 0, sprite, layer = layer)

    def _draw_forecast(self, forecast:WeatherData) -> None:
        self._canvas.clear_layer(Layer.Middle)
        self._draw_temperature(17, 2, forecast.night_temp_c)
        self._draw_temperature(17, 14, forecast.day_temp_c)
        self._draw_wind(36, 14, forecast.wind_speed_knts, forecast.wind_direction)
        self._draw_weather_symbol(0, 31, forecast.day_weather)
        self._draw_weather_symbol(33, 31, forecast.night_weather)

    def _draw_temperature(self, x:int, y:int, temperature:int) -> None:
        colour = get_colour_for_temperature(temperature)
        temp_value = abs(temperature)
        self._canvas.draw_leading_space_digits(x, y, colour, digit_width = 2, number = temp_value, layer = Layer.Middle)
        if temperature < 0:
            self._draw_negative_sign(x - 3, y + 4, colour)

    def _draw_negative_sign(self, x:int, y:int, colour:RGBColour) -> None:
        self._canvas.draw_horizontal_line(x, y, 2, colour, layer = Layer.Middle)

    def _draw_wind(self, x:int, y:int, speed:int, direction:int):
        colour = get_colour_for_speed(speed)
        if speed > 0:
            sprite = get_coloured_compass_sprite(direction, BLACK, colour)
            self._canvas.draw_sprite(x, y + 1, sprite, layer = Layer.Middle)

        self._canvas.draw_leading_space_digits(x + 9, y, colour, digit_width = 3, number = speed, layer = Layer.Middle)

    def _draw_weather_symbol(self, x:int, y:int, symbol_id:str):
        if not symbol_id in self._weather_symbol_sprites:
            image = Image.open(f'images/weather/{symbol_id}.png').convert('RGB')
            new_sprite = create_sprite_from_image(image)
            self._weather_symbol_sprites[symbol_id] = new_sprite

        sprite = self._weather_symbol_sprites[symbol_id]
        self._canvas.draw_sprite(x, y, sprite, layer = Layer.Middle)
