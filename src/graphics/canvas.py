import time
from enum import Enum
from typing import Any, Callable, Generator

from graphics.colours import BLACK, RGBColour
from graphics.numbers import get_coloured_digit_sprite
from graphics.sprites import Sprite

LayerMatrix = list[ list[ RGBColour ]]

class Layer(Enum):
    Bottom = 0,
    Middle = 1,
    Top = 2,
    Debug = 3

class Canvas:
    def __init__(self, width:int, height:int, debug_update:Callable[[Any], None]):
        self._width = width
        self._height = height
        self._debug_update = debug_update
        self.clear_all()

    def clear_all(self) -> None:
        self._debug_layer = LayerMatrix()
        self._top_layer = LayerMatrix()
        self._middle_layer = LayerMatrix()
        self._bottom_layer = LayerMatrix()

        for _ in range(self._height):
            self._debug_layer.append(self._black_row())
            self._top_layer.append(self._black_row())
            self._middle_layer.append(self._black_row())
            self._bottom_layer.append(self._black_row())

    def clear_layer(self, layer:Layer) -> None:
        matrix:list[list[RGBColour]] = []
        for _ in range(self._height):
            matrix.append(self._black_row())

        if layer == Layer.Bottom:
            self._bottom_layer = matrix
        elif layer == Layer.Middle:
            self._middle_layer = matrix
        elif layer == Layer.Top:
            self._top_layer = matrix
        else:
            self._debug_layer = matrix

    def set_pixel(self, x:int, y:int, colour:RGBColour, *, layer:Layer) -> None:
        self._selected_layer(layer)[y][x] = colour

    def get_pixel(self, x:int, y:int, *, layer:Layer) -> RGBColour:
        return self._selected_layer(layer)[y][x]

    def draw_horizontal_line(self, x:int, y:int, width:int, colour:RGBColour, *, layer:Layer) -> None:
        selected_layer = self._selected_layer(layer)
        for offset in range(width):
            self._set_pixel(selected_layer, x + offset, y, colour)

    def draw_vertical_line(self, x:int, y:int, height:int, colour:RGBColour, *, layer:Layer) -> None:
        selected_layer = self._selected_layer(layer)
        for offset in range(height):
            self._set_pixel(selected_layer, x, y + offset, colour)

    def flood_fill(self, x:int, y:int, width:int, height:int, colour:RGBColour, *, layer:Layer) -> None:
        selected_layer = self._selected_layer(layer)
        for offset_y in range(height):
            for offset_x in range(width):
                self._set_pixel(selected_layer, x + offset_x, y + offset_y, colour)

    def draw_sprite(self, x:int, y:int, sprite:Sprite, *, layer:Layer) -> None:
        selected_layer = self._selected_layer(layer)
        for i, row in enumerate(sprite):
            for j, colour in enumerate(row):
                self._set_pixel(selected_layer, x + j, y + i, colour)

    def draw_transparent_sprite(self, x:int, y:int, sprite:Sprite, *, layer:Layer) -> None:
        selected_layer = self._selected_layer(layer)
        for i, row in enumerate(sprite):
            for j, colour in enumerate(row):
                if colour != BLACK:
                    self._set_pixel(selected_layer, x + j, y + i, colour)

    def render_as_bytes(self) -> bytes:
        def pixel_colours() -> Generator[RGBColour, None, None]:
            for y in range(self._height):
                for x in range(self._width):
                    yield self._check_layers_for_coloured_pixel(x, y)

        self._debug_update(self)
        return b''.join([p.to_bytes(3, 'big') for p in pixel_colours()])

    def copy_transform_paste_layer(
        self, 
        *, 
        from_layer:Layer, 
        to_layer:Layer, 
        transform:Callable[[RGBColour], RGBColour]
    ) -> None:
        for y in range(self._height):
            for x in range(self._width):
                pixel = self.get_pixel(x, y, layer = from_layer)
                self.set_pixel(x, y, transform(pixel), layer = to_layer)
    
    def copy_paste_layer(self, *, from_layer:Layer, to_layer:Layer):
        self.copy_transform_paste_layer(from_layer = from_layer, to_layer = to_layer, transform = lambda x: x)
    
    def draw_leading_zero_digits(
        self, 
        x:int, 
        y:int, 
        colour:RGBColour, 
        *, 
        digit_width:int, 
        number:int,
        layer:Layer
    ) -> None:
        digits = [int(d) for d in f"{number:0{digit_width}d}"]
        for i in range(digit_width):
            sprite = get_coloured_digit_sprite(digits[i], BLACK, colour)
            self.draw_sprite(i * 6 + x, y, sprite, layer = layer)
    
    def draw_leading_space_digits(
        self, 
        x:int, 
        y:int, 
        colour:RGBColour, 
        *, 
        digit_width:int, 
        number:int,
        layer:Layer
    ) -> None:
        digits = [d for d in f"{number:{digit_width}d}"]
        for i in range(digit_width):
            if digits[i] != ' ':
                sprite = get_coloured_digit_sprite(int(digits[i]), BLACK, colour)
                self.draw_sprite(i * 6 + x, y, sprite, layer = layer)

    def draw_time(self, x:int, y:int, colour:RGBColour, current_time:float):
        timeval = time.localtime(current_time)
        self.draw_leading_zero_digits(x, y, colour, digit_width = 2, number = timeval.tm_hour, layer = Layer.Top)
        self.draw_leading_zero_digits(x + 14, y, colour, digit_width = 2, number = timeval.tm_min, layer = Layer.Top)
        self._draw_seconds_line(s if (s := timeval.tm_sec) > 0 else 60, colour)

    def _draw_seconds_line(self, seconds:int, colour:RGBColour) -> None:
        self.draw_horizontal_line(2, 0, 60, BLACK, layer = Layer.Top)
        self.draw_horizontal_line(2, 0, seconds, colour, layer = Layer.Top)

    def _selected_layer(self, layer:Layer) -> LayerMatrix:
        if layer == Layer.Bottom:
            return self._bottom_layer
        elif layer == Layer.Middle:
            return self._middle_layer
        elif layer == Layer.Top:
            return self._top_layer
        else:
            return self._debug_layer

    def _black_row(self) -> list[RGBColour]:
        row:list[RGBColour] = []
        for _ in range(self._width):
            row.append(BLACK)
        return row

    def _set_pixel(self, layer:LayerMatrix, x:int, y:int, colour:RGBColour) -> None:
        layer[y][x] = colour

    def _check_layers_for_coloured_pixel(self, x:int, y:int) -> RGBColour:
        if (d := self._debug_layer[y][x]) and d != BLACK:  
            return d
        if (t := self._top_layer[y][x]) and t != BLACK:  
            return t
        if (m := self._middle_layer[y][x]) and m != BLACK: 
            return m
        else:
            return self._bottom_layer[y][x]