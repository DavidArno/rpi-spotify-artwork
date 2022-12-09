from math import sqrt


INVADER_ROWS = 6
INVADERS_PER_ROW = 7
MAXIMUM_BOMBS = 5
MAXIMUM_INVADERS = INVADERS_PER_ROW * INVADER_ROWS


def _tick_delay_for_number_invaders(num_invaders: int) -> int:
    value1 = int(num_invaders / MAXIMUM_INVADERS * 20 + 0.5)
    value2 = int(sqrt(num_invaders) / sqrt(MAXIMUM_INVADERS) * 20 - 2.5)
    return max(value1, value2)


TICKS_BETWEEN_INVADER_MOVES = [_tick_delay_for_number_invaders(t) for t in range(MAXIMUM_INVADERS + 1)]
TICKS_BETWEEN_BOMB_MOVES = 1
TICKS_BETWEEN_MISSILE_MOVES = 1
TICKS_BETWEEN_PLAYER_MOVES = 0
TICKS_BETWEEN_SAUCER_MOVES = 5

RANDOM_RANGE_FOR_BOMB_DROP = 25
RANDOM_RANGE_FOR_SAUCER_APPEARANCE = 100

