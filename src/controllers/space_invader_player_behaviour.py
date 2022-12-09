################################################################################
# inputs:
# invader positions
# bomb positions
# missile position
# vertical "line of sight" (to determine if missile would hit a defence tower)
################################################################################
# Strategy:
# Will always try to take out the "leading edge" invaders so will follow their
# movement. It will randmly favour the right or left leading edge and stick to
# that throughout a round
# Will avoid shooting the towers
# Will move aside from the lowest missile and will move in the opposite
# direction of the second lowest unless this causes it to hit the edge of the
# screen. Will try to continue following the leading edge unless that puts it
# back in line to be hit.
################################################################################
from controllers.space_invaders_controller import Munition
from graphics.invaders import MISSILE_LAUNCHER_WIDTH


class PlayerBehaviour:
    _launcher_x: int
    _launcher_y: int

    def _try_calculate_ticks_until_bomb_impacts_launcher(self, bombs: list[Munition]) -> None | int:
        if len(bombs) == 0:
            return None

        lowest_bomb_x = -1
        lowest_bomb_y = 0
        second_lowest_bomb_x = -1

        for bomb in bombs:
            if lowest_bomb_x is None:
                lowest_bomb_x = bomb.x
                lowest_bomb_y = bomb.y
            elif bomb.x > lowest_bomb_x:
                second_lowest_bomb_x = lowest_bomb_x
                lowest_bomb_x = bomb.x
                lowest_bomb_y = bomb.y

        if not self._launcher_x <= lowest_bomb_x <= self._launcher_x + MISSILE_LAUNCHER_WIDTH:
            return None

