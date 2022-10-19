from dataclasses import dataclass
from random import randint
from typing import Callable

from PIL import Image  # type: ignore

from graphics.canvas import Canvas, Layer
from graphics.colours import BLACK, WHITE, RGBColour
from graphics.invaders import (INVADER_HEIGHT, INVADER_WIDTH,
                               get_coloured_defence_tower_sprite,
                               get_coloured_invader_sprite,
                               get_coloured_missile_launcher_sprite,
                               get_coloured_saucer_sprite)
from graphics.sprites import Sprite, create_coloured_sprite_from_mono_image

_SPACE_INVADER_RED = RGBColour(0xEA1B2C)
_SPACE_INVADER_ORANGE = RGBColour(0xF37618)
_SPACE_INVADER_YELLOW = RGBColour(0xFEF100)
_SPACE_INVADER_GREEN = RGBColour(0x39FE49)
_SPACE_INVADER_CYAN = RGBColour(0x04BAEA)

_CRAB = 0
_JELLYFISH = 2
_SQUID = 4

_INVADERS_PER_ROW = 7
_INVADER_COLOURS = [
    _SPACE_INVADER_YELLOW,
    _SPACE_INVADER_YELLOW,
    _SPACE_INVADER_ORANGE,
    _SPACE_INVADER_ORANGE,
    _SPACE_INVADER_GREEN,
    _SPACE_INVADER_GREEN
]

_STARTING_NUMBER_OF_INVADERS = _INVADERS_PER_ROW * len(_INVADER_COLOURS)

@dataclass
class Invader(): 
    index: int
    x: int
    y: int
    alive: bool
    shooter: bool

class SpaceInvadersController():
    _invaders:list[Invader] = []
    _missile_x: int
    _missile_y: int
    _left_to_right: bool
    _invader_sprites:list[Sprite]
    _shooter_sprites:list[Sprite]
    _alive_invaders:int = _STARTING_NUMBER_OF_INVADERS
    _ticks_to_next_move:int
    _game_over:bool = False

    def __init__(self, canvas:Canvas, check_enabled:Callable[[], bool]):
        self._canvas = canvas
        self._check_enabled = check_enabled
        self._setup_invaders()

    def actively_displaying(self, _:float) -> bool:
        if not self._check_enabled(): return False
        if self._game_over: return True

        self._update_invaders_and_missile_state()
        self._render_game_board()

        return True

    def _setup_invaders(self) -> None:
        invaders = [_JELLYFISH, _CRAB, _CRAB, _SQUID, _SQUID]
        for y in range(5):
            for x in range (_INVADERS_PER_ROW):
                self._invaders.append(Invader(invaders[y], 12 + 7 * x, 6 + 7 * y, True, False))

        self._missile_x = -1
        self._left_to_right = True
        self._ticks_to_next_move = self._get_ticks_to_next_invader_move()

        self._invader_sprites = [get_coloured_invader_sprite(i, BLACK, _INVADER_COLOURS[i]) for i in range(6)]
        self._shooter_sprites = [get_coloured_invader_sprite(i, BLACK, WHITE) for i in range(6)]

        defence_tower = get_coloured_defence_tower_sprite(BLACK, _SPACE_INVADER_CYAN)
        for x in range(3):
            self._canvas.draw_sprite(8 + 20 * x, 51, defence_tower, layer = Layer.Middle)

        missile_launcher = get_coloured_missile_launcher_sprite(BLACK, _SPACE_INVADER_CYAN)
        self._canvas.draw_sprite(40, 61, missile_launcher, layer = Layer.Top)

        saucer = get_coloured_saucer_sprite(BLACK, _SPACE_INVADER_RED)
        self._canvas.draw_sprite(20, 0, saucer, layer = Layer.Top)

        game_over = Image.open(f'images/invaders/game_over.png').convert('RGB')
        self._game_over_sprite = create_coloured_sprite_from_mono_image(game_over, foreground_colour = _SPACE_INVADER_RED)

    def _get_ticks_to_next_invader_move(self): 
        return int(self._alive_invaders / _STARTING_NUMBER_OF_INVADERS * 20 - 0.5)

    def _update_invaders_and_missile_state(self) -> None:
        nearest_to_edge = 0 if self._left_to_right else 63
        self._invaders_able_to_shoot = []

        self._ticks_to_next_move -= 1
        move_x = 0
        invaders_alive = 0

        if self._ticks_to_next_move <= 0:
             self._ticks_to_next_move = self._get_ticks_to_next_invader_move()
             move_x = 1 if self._left_to_right else -1

        invaders_able_to_shoot:list[Invader] = []
        for invader in self._invaders:
            if invader.alive and \
               self._missile_active() and \
               self._check_collision(self._missile_x, self._missile_y, invader.x, invader.y):
                self._explode(invader)
            
            if randint(1, 500) == 500:
                invader.alive = False
                
            if invader.alive:
                invaders_alive += 1
                invader.shooter = False
                if move_x != 0:
                    invader.index = self._flip_sprite_index(invader.index)

                invader.x += move_x
                nearest_to_edge = self._nearest_to_edge(nearest_to_edge, invader.x, self._left_to_right)

                add_to_shooters = True
                for i, shooter in enumerate(invaders_able_to_shoot):
                    if shooter.x == invader.x:
                        add_to_shooters = False
                        if shooter.y < invader.y:
                            invaders_able_to_shoot[i] = invader
                
                if add_to_shooters:
                    invaders_able_to_shoot.append(invader)
        
        self._alive_invaders = invaders_alive
        ticks_between_moves = self._get_ticks_to_next_invader_move()
        if ticks_between_moves < self._ticks_to_next_move:
            self._ticks_to_next_move = ticks_between_moves

        if (self._left_to_right and nearest_to_edge == 58) or (nearest_to_edge == 0):
            self._left_to_right = not self._left_to_right
            for invader in self._invaders:
                if invader.alive:
                    invader.y += 1

        for invader in invaders_able_to_shoot:
            invader.shooter = True

    def _render_game_board(self) -> None:
        self._canvas.clear_layer(Layer.Bottom)
        for invader in self._invaders:
            if invader.alive:
                if invader.y >= 64 - INVADER_HEIGHT:
                    self._handle_game_over()
                    return
                if invader.shooter:
                    self._canvas.draw_sprite(invader.x, invader.y, self._shooter_sprites[invader.index], layer = Layer.Bottom)
                    self._canvas.flood_fill(invader.x, invader.y, INVADER_WIDTH, INVADER_HEIGHT, BLACK, layer = Layer.Middle)
                else:
                    self._canvas.draw_sprite(invader.x, invader.y, self._invader_sprites[invader.index], layer = Layer.Bottom)

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

    def _handle_game_over(self):
        self._canvas.draw_transparent_sprite(19, 4, self._game_over_sprite, layer = Layer.Top)
        self._game_over = True
