from typing import Callable, Generator
from graphics.colours import BLACK, RGBColour
from graphics.sprites import Sprite
from enum import Enum

LayerMatrix = list[ list[ RGBColour ]]

class Layer(Enum):
    Bottom = 0,
    Middle = 1,
    Top = 2

class Canvas:
    def __init__(self, width:int, height:int):
        self._width = width
        self._height = height
        self.clear_all()

    def clear_all(self) -> None:
        self._top_layer = LayerMatrix()
        self._middle_layer = LayerMatrix()
        self._bottom_layer = LayerMatrix()

        for _ in range(self._height):
            self._top_layer.append(self._black_row())
            self._middle_layer.append(self._black_row())
            self._bottom_layer.append(self._black_row())

    def clear_layer(self, layer:Layer) -> None:
        matrix = []
        for _ in range(self._height):
            matrix.append(self._black_row())

        if layer == Layer.Bottom:
            self._bottom_layer = matrix
        elif layer == Layer.Middle:
            self._middle_layer = matrix
        else:
            self._top_layer = matrix

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

    def render_as_bytes(self) -> bytes:
        def pixel_colours(self) -> Generator[RGBColour, None, None]:
            for y in range(self._height):
                for x in range(self._width):
                    yield self._check_layers_for_coloured_pixel(x, y)

        return b''.join([p.to_bytes(3, 'big') for p in pixel_colours(self)])

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

    def _selected_layer(self, layer:Layer) -> LayerMatrix:
        if layer == Layer.Bottom:
            return self._bottom_layer
        elif layer == Layer.Middle:
            return self._middle_layer
        else:
            return self._top_layer

    def _black_row(self) -> list[RGBColour]:
        row:list[RGBColour] = []
        for _ in range(self._width):
            row.append(BLACK)
        return row

    def _set_pixel(self, layer:LayerMatrix, x:int, y:int, colour:RGBColour) -> None:
        layer[y][x] = colour

    def _check_layers_for_coloured_pixel(self, x:int, y:int) -> RGBColour:
        if (t := self._top_layer[y][x]) and t != BLACK:  
            return t
        if (m := self._middle_layer[y][x]) and m != BLACK: 
            return m
        else:
            return self._bottom_layer[y][x]