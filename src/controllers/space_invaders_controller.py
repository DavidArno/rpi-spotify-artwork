from dataclasses import dataclass
from enum import Enum
from random import randint
from typing import Callable

from PIL import Image  # type:ignore
from controllers.space_invader_parameters import \
        INVADER_ROWS, INVADERS_PER_ROW, MAXIMUM_BOMBS, MAXIMUM_INVADERS, TICKS_BETWEEN_INVADER_MOVES

from common.graphics.canvas import Canvas, Layer
from common.graphics.colours import BLACK, WHITE, RGBColour
from graphics.invaders import (BOMB_HEIGHT, BOMB_WIDTH, INVADER_HEIGHT, INVADER_WIDTH, MISSILE_LAUNCHER_WIDTH,
                               get_coloured_bomb_sprite,
                               get_coloured_dead_launcher_sprite,
                               get_coloured_defence_tower_sprite,
                               get_coloured_invader_sprite,
                               get_coloured_missile_launcher_sprite, get_coloured_missile_sprite,
                               get_coloured_saucer_sprite)
from common.graphics.sprites import Sprite, create_coloured_sprite_from_mono_image

_SPACE_INVADER_RED = RGBColour(0xEA1B2C)
_SPACE_INVADER_ORANGE = RGBColour(0xF37618)
_SPACE_INVADER_YELLOW = RGBColour(0xFEF100)
_SPACE_INVADER_GREEN = RGBColour(0x39FE49)
_SPACE_INVADER_CYAN = RGBColour(0x04BAEA)

_CRAB = 0
_JELLYFISH = 2
_SQUID = 4


_INVADER_COLOURS = [
    _SPACE_INVADER_YELLOW,
    _SPACE_INVADER_YELLOW,
    _SPACE_INVADER_ORANGE,
    _SPACE_INVADER_ORANGE,
    _SPACE_INVADER_GREEN,
    _SPACE_INVADER_GREEN
]

if INVADER_ROWS != len(_INVADER_COLOURS):
    raise RuntimeError(f"INVADER_ROWS ({INVADER_ROWS}) and _INVADER_COLOURS ({len(_INVADER_COLOURS)}) do not match")


@dataclass
class Invader:
    index: int
    x: int
    y: int
    alive: bool
    shooter: bool


@dataclass
class Munition:
    x: int
    y: int
    active: bool


class LauncherState(Enum):
    Alive = 0,
    Hit = 1,
    Dead = 2


@dataclass
class Player:
    missile_x: int
    missile_y: int
    missile_in_flight: bool
    missile_sprite: Sprite
    launcher_x: int
    launcher_state: LauncherState
    launcher_sprite: Sprite
    dead_launcher_sprite: Sprite


class SpaceInvadersController:
    _invaders: list[Invader] = []
    _left_to_right: bool
    _invader_sprites: list[Sprite]
    _shooter_sprites: list[Sprite]
    _bomb_sprite: Sprite
    _alive_invaders: int = MAXIMUM_INVADERS
    _ticks_to_next_move: int
    _game_over: bool = False
    _bombs: list[Munition] = []
    _invaders_able_to_shoot: list[Invader] = []
    _bomb_move: bool
    _player: Player

    def __init__(self, canvas: Canvas, check_enabled: Callable[[], bool]):
        self._canvas = canvas
        self._check_enabled = check_enabled
        self._setup_invaders()
        self._setup_player()

    def actively_displaying(self, _: float) -> bool:
        if not self._check_enabled():
            return False

        if self._game_over:
            return True

        self._update_invaders_state()
        self._update_bombs_state()
        self._render_game_board()

        return True

    def _setup_invaders(self) -> None:
        invaders = [_JELLYFISH, _CRAB, _CRAB, _SQUID, _SQUID]
        for y in range(5):
            for x in range(INVADERS_PER_ROW):
                self._invaders.append(Invader(invaders[y], 12 + 7 * x, 6 + 7 * y, True, False))

        self._left_to_right = True
        self._ticks_to_next_move = self._get_ticks_to_next_invader_move()

        self._invader_sprites = [get_coloured_invader_sprite(i, BLACK, _INVADER_COLOURS[i]) for i in range(6)]
        self._shooter_sprites = [get_coloured_invader_sprite(i, BLACK, WHITE) for i in range(6)]

        self._bomb_sprite = get_coloured_bomb_sprite(WHITE, BLACK)
        self._bomb_move = False

        defence_tower = get_coloured_defence_tower_sprite(BLACK, _SPACE_INVADER_CYAN)
        for x in range(3):
            self._canvas.draw_sprite(8 + 20 * x, 51, defence_tower, layer=Layer.Middle)

        saucer = get_coloured_saucer_sprite(BLACK, _SPACE_INVADER_RED)
        self._canvas.draw_sprite(20, 0, saucer, layer=Layer.Top)

        game_over = Image.open(f'images/invaders/game_over.png').convert('RGB')
        self._game_over_sprite = create_coloured_sprite_from_mono_image(game_over, foreground_colour=_SPACE_INVADER_RED)

    def _setup_player(self):
        self._player = Player(
            missile_x=0,
            missile_y=0,
            missile_in_flight=False,
            missile_sprite=get_coloured_missile_sprite(BLACK, WHITE),
            launcher_x=32 + int(MISSILE_LAUNCHER_WIDTH/2),
            launcher_state=LauncherState.Alive,
            launcher_sprite=get_coloured_missile_launcher_sprite(BLACK, _SPACE_INVADER_CYAN),
            dead_launcher_sprite=get_coloured_dead_launcher_sprite(BLACK, _SPACE_INVADER_CYAN)
        )

    def _get_ticks_to_next_invader_move(self):
        return TICKS_BETWEEN_INVADER_MOVES[self._alive_invaders]

    def _update_invaders_state(self) -> None:
        nearest_to_edge = 0 if self._left_to_right else 63
        self._invaders_able_to_shoot = []

        self._ticks_to_next_move -= 1
        move_x = 0

        if self._ticks_to_next_move <= 0:
            self._ticks_to_next_move = self._get_ticks_to_next_invader_move()
            move_x = 1 if self._left_to_right else -1

        for invader in self._invaders:
            if invader.alive and \
               self._player.missile_in_flight and \
               self._check_collision(self._player.missile_x, self._player.missile_y, invader.x, invader.y):
                self._explode(invader)

            if randint(1, 500) == 500:
                invader.alive = False

            if invader.alive:
                invader.shooter = False
                if move_x != 0:
                    invader.index = self._flip_sprite_index(invader.index)

                invader.x += move_x
                nearest_to_edge = self._nearest_to_edge(nearest_to_edge, invader.x, self._left_to_right)

                add_to_shooters = True
                for i, shooter in enumerate(self._invaders_able_to_shoot):
                    if shooter.x == invader.x:
                        add_to_shooters = False
                        if shooter.y < invader.y:
                            self._invaders_able_to_shoot[i] = invader

                if add_to_shooters:
                    self._invaders_able_to_shoot.append(invader)

        self._invaders = [i for i in self._invaders if i.alive]
        self._alive_invaders = len(self._invaders)
        ticks_between_moves = self._get_ticks_to_next_invader_move()
        if ticks_between_moves < self._ticks_to_next_move:
            self._ticks_to_next_move = ticks_between_moves

        if (self._left_to_right and nearest_to_edge == 58) or (nearest_to_edge == 0):
            self._left_to_right = not self._left_to_right
            for invader in self._invaders:
                invader.y += 1

        for invader in self._invaders_able_to_shoot:
            invader.shooter = True

    def _update_bombs_state(self):
        if len(self._bombs) < MAXIMUM_BOMBS:
            if randint(1, 25) == 25:
                shooter_index = randint(0, len(self._invaders_able_to_shoot)-1)
                shooter = self._invaders_able_to_shoot[shooter_index]
                x = shooter.x + int(INVADER_WIDTH/2)
                y = shooter.y + INVADER_HEIGHT
                self._bombs.append(Munition(x, y, True))

        if self._bomb_move:
            for bomb in self._bombs:
                bomb.y += 1
                if bomb.y >= 64 - BOMB_HEIGHT:
                    bomb.active = False

        self._bomb_move = not self._bomb_move
        self._bombs = [b for b in self._bombs if b.active]

    def _render_game_board(self) -> None:
        self._canvas.clear_layer(Layer.Bottom)
        self._canvas.clear_layer(Layer.Top)

        if self._player.launcher_state == LauncherState.Alive:
            self._canvas.draw_sprite(self._player.launcher_x, 61, self._player.launcher_sprite, layer=Layer.Top)
        elif self._player.launcher_state == LauncherState.Hit:
            self._canvas.draw_sprite(
                self._player.launcher_x - 1,
                60,
                self._player.dead_launcher_sprite,
                layer=Layer.Top
            )
        for invader in self._invaders:
            if invader.y >= 64 - INVADER_HEIGHT:
                self._handle_game_over()
                return

            if invader.shooter:
                self._canvas.draw_sprite(
                    invader.x,
                    invader.y,
                    self._shooter_sprites[invader.index],
                    layer=Layer.Bottom
                )

                self._canvas.flood_fill(
                    invader.x,
                    invader.y,
                    INVADER_WIDTH,
                    INVADER_HEIGHT,
                    BLACK,
                    layer=Layer.Middle
                )
            else:
                self._canvas.draw_sprite(
                    invader.x,
                    invader.y,
                    self._invader_sprites[invader.index],
                    layer=Layer.Bottom
                )

        for bomb in self._bombs:
            if self._canvas.get_pixel(bomb.x, bomb.y + BOMB_HEIGHT - 1, layer=Layer.Middle) != BLACK or \
               self._canvas.get_pixel(bomb.x+1, bomb.y + BOMB_HEIGHT - 1, layer=Layer.Middle) != BLACK:
                bomb.active = False
                self._canvas.flood_fill(
                    bomb.x,
                    bomb.y,
                    BOMB_WIDTH,
                    BOMB_HEIGHT,
                    BLACK,
                    layer=Layer.Middle
                )
            elif (self._canvas.get_pixel(bomb.x, bomb.y + BOMB_HEIGHT - 1, layer=Layer.Top) == _SPACE_INVADER_CYAN or
                  self._canvas.get_pixel(bomb.x+1, bomb.y + BOMB_HEIGHT - 1, layer=Layer.Top) == _SPACE_INVADER_CYAN):
                bomb.active = False
                self._player.launcher_state = LauncherState.Hit
            else:
                self._canvas.draw_sprite(
                    bomb.x,
                    bomb.y,
                    self._bomb_sprite,
                    layer=Layer.Bottom
                )

    def _check_collision(self, missile_top_x: int, missile_top_y: int, invader_x: int, invader_y: int) -> bool:
        rect_x1 = invader_x
        rect_y1 = invader_y
        rect_x2 = rect_x1 + 4
        rect_y2 = rect_y1 + 4
        miss_x = missile_top_x
        miss_y1 = missile_top_y
        miss_y2 = miss_y1 + 2
        return (rect_x1 <= miss_x <= rect_x2 and rect_y1 <= miss_y1 <= rect_y2) or \
               (rect_x1 <= miss_x <= rect_x2 and rect_y1 <= miss_y2 <= rect_y2)

    def _explode(self, invader: Invader):
        invader.alive = False
        self._player.missile_x = -1
        #draw explosion

    def _flip_sprite_index(self, index: int) -> int:
        return index + 1 if index % 2 == 0 else index - 1

    def _nearest_to_edge(self, x1: int, x2: int, left_to_right: bool):
        if left_to_right:
            return x1 if x1 > x2 else x2
        else:
            return x1 if x1 < x2 else x2

    def _handle_game_over(self):
        self._canvas.draw_transparent_sprite(22, 4, self._game_over_sprite, layer=Layer.Top)
        self._game_over = True
