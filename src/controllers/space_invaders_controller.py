from dataclasses import dataclass
from typing import Callable

from graphics.canvas import Canvas, Layer
from graphics.colours import BLACK, RGBColour
from graphics.invaders import get_coloured_alien_sprite
from graphics.sprites import Sprite

_SPACE_INVADER_RED = RGBColour(0xEA1B2C)
_SPACE_INVADER_ORANGE = RGBColour(0xF37618)
_SPACE_INVADER_YELLOW = RGBColour(0xFEF100)
_SPACE_INVADER_GREEN = RGBColour(0x39FE49)
_SPACE_INVADER_CYAN = RGBColour(0x04BAEA)

_JELLYFISH = 2
_CRAB = 0
_SQUID = 4

_INVADERS_PER_ROW = 1

@dataclass
class Invader(): 
    index: int
    x: int
    y: int
    alive: bool

class SpaceInvadersController():
    _invaders:list[Invader] = []
    _missile_x: int
    _missile_y: int
    _left_to_right: bool
    _alien_sprites:list[Sprite]
    
    def __init__(self, canvas:Canvas, check_enabled:Callable[[], bool]):
        self._canvas = canvas
        self._check_enabled = check_enabled
        self._setup_invaders()
        
    def actively_displaying(self, _:float) -> bool:
        if not self._check_enabled(): return False

        self._update_invaders_and_missile_state()
        self._render_game_board()

        return True

    def _setup_invaders(self) -> None:
        aliens = [_JELLYFISH, _CRAB, _CRAB, _SQUID, _SQUID]
        for y in range(5):
            for x in range (_INVADERS_PER_ROW):
                self._invaders.append(Invader(aliens[y], 12 + 7 * x, 5 + 7 * y, True))

        self._missile_x = -1
        self._left_to_right = True

        colours = [
            _SPACE_INVADER_YELLOW,
            _SPACE_INVADER_YELLOW,
            _SPACE_INVADER_ORANGE,
            _SPACE_INVADER_ORANGE,
            _SPACE_INVADER_GREEN,
            _SPACE_INVADER_GREEN
        ]

        self._alien_sprites = [get_coloured_alien_sprite(i, BLACK, colours[i]) for i in range(6)]

    def _update_invaders_and_missile_state(self) -> None:
        nearest_to_edge = 0 if self._left_to_right else 63

        for invader in self._invaders:
            if invader.alive and \
               self._missile_active() and \
               self._check_collision(self._missile_x, self._missile_y, invader.x, invader.y):
                self._explode(invader)
                
            if invader.alive:
                invader.index = self._flip_sprite_index(invader.index)
                invader.x += 1 if self._left_to_right else -1
                nearest_to_edge = self._nearest_to_edge(nearest_to_edge, invader.x, self._left_to_right)
        
        if (self._left_to_right and nearest_to_edge == 58) or (nearest_to_edge == 1):
            self._left_to_right = not self._left_to_right
            for invader in self._invaders:
                if invader.alive:
                    invader.y += 1

    def _render_game_board(self) -> None:
        self._canvas.clear_layer(Layer.Bottom)
        for invader in self._invaders:
            if invader.alive:
                self._canvas.draw_sprite(invader.x, invader.y, self._alien_sprites[invader.index], layer = Layer.Bottom)

    def _missile_active(self) -> bool: return self._missile_x > -1

    def _check_collision(self, missile_top_x:int, missile_top_y:int, invader_x:int, invader_y:int) -> bool:
        rect_x1 = invader_x
        rect_y1 = invader_y
        rect_x2 = rect_x1 + 4
        rect_y2 = rect_y1 + 4
        miss_x = missile_top_x
        miss_y1 = missile_top_y
        miss_y2 = miss_y1 + 2 
        return (rect_x1 <= miss_x <= rect_x2 and rect_y1 <= miss_y1 <= rect_y2) or \
               (rect_x1 <= miss_x <= rect_x2 and rect_y1 <= miss_y2 <= rect_y2)

    def _explode(self, invader:Invader):
        invader.alive = False
        self._missile_x = -1
        #draw explosion

    def _flip_sprite_index(self, index:int) -> int:
        return index + 1 if index % 2 == 0 else index - 1

    def _nearest_to_edge(self, x1:int, x2:int, left_to_right:bool):
        if left_to_right:
            return x1 if x1 > x2 else x2
        else:
            return x1 if x1 < x2 else x2