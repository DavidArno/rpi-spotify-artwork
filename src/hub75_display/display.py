import compatibility

import hub75 # type: ignore
from hub75_display.colours import Hub75Colour, BLACK
from hub75_display.sprites import Sprite

if compatibility.running_as_cpython:
    LayerMatrix = list[ list[ Hub75Colour ]] # type: ignore
    from enum import Enum
else:
    LayerMatrix = object # type: ignore
    Enum = object # type: ignore

class Layer(Enum):
    Bottom = 0,
    Middle = 1,
    Top = 2

class Display:
    def __init__(
        self, 
        width:int, 
        height:int, 
        hub:hub75.Hub75
    ):
        self._width = width
        self._height = height
        self._hub = hub

        self.clear_all()

    def clear_all(self) -> None:
        self._top_layer = [] # type: LayerMatrix
        self._middle_layer = [] # type: LayerMatrix
        self._bottom_layer = [] # type: LayerMatrix

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

    def set_pixel(self, x:int, y:int, colour:Hub75Colour, *, layer:Layer) -> None:
        self._selected_layer(layer)[y][x] = colour

    def get_pixel(self, x:int, y:int, *, layer:Layer) -> Hub75Colour:
        return self._selected_layer(layer)[y][x]

    def draw_horizontal_line(self, x:int, y:int, width:int, colour:Hub75Colour, *, layer:Layer) -> None:
        selected_layer = self._selected_layer(layer)
        for offset in range(width):
            self._set_pixel(selected_layer, x + offset, y, colour)

    def draw_vertical_line(self, x:int, y:int, height:int, colour:Hub75Colour, *, layer:Layer) -> None:
        selected_layer = self._selected_layer(layer)
        for offset in range(height):
            self._set_pixel(selected_layer, x, y + offset, colour)

    def flood_fill(self, x:int, y:int, width:int, height:int, colour:Hub75Colour, *, layer:Layer) -> None:
        selected_layer = self._selected_layer(layer)
        for offset_y in range(height):
            for offset_x in range(width):
                self._set_pixel(selected_layer, x + offset_x, y + offset_y, colour)

    def draw_sprite(self, x:int, y:int, sprite:Sprite, *, layer:Layer) -> None:
        selected_layer = self._selected_layer(layer)
        for i, row in enumerate(sprite):
            for j, colour in enumerate(row):
                self._set_pixel(selected_layer, x + j, y + i, colour)

    def render_display(self):
        for y in range(self._height):
            for x in range(self._width):
                colour = self._check_layers_for_coloured_pixel(x, y)
                self._hub.set_color(x, y, colour)

        self._hub.flip_and_clear(BLACK)

    def _selected_layer(self, layer:Layer) -> LayerMatrix:
        if layer == Layer.Bottom:
            return self._bottom_layer
        elif layer == Layer.Middle:
            return self._middle_layer
        else:
            return self._top_layer

    def _black_row(self) -> 'list[Hub75Colour]':
        row:list[Hub75Colour] = [] # type: ignore
        for _ in range(self._width):
            row.append(BLACK)
        return row

    def _set_pixel(self, layer:LayerMatrix, x:int, y:int, colour:Hub75Colour) -> None:
        layer[y][x] = colour

    def _check_layers_for_coloured_pixel(self, x:int, y:int):
        if (t := self._top_layer[y][x]) and t != BLACK:  # type: ignore
            return t
        if (m := self._middle_layer[y][x]) and m != BLACK:  # type: ignore
            return m
        else:
            return self._bottom_layer[y][x]