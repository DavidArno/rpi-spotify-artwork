from enum import Enum
import hub75

from hub75_display.display import Display # type: ignore

class PanelType(Enum):
    Generic = 0,
    FM6126A = 1

class LedMatrix:
    def __init__(
        self, 
        width:int, 
        height:int, 
        panel_type:PanelType = PanelType.Generic, 
        stb_invert:bool = False
    ):
        self._width = width
        self._height = height
        self._hub = hub75.Hub75(
            width, 
            height, 
            stb_invert = stb_invert, 
            panel_type = hub75.PANEL_GENERIC if panel_type == PanelType.Generic else hub75.PANEL_FM6126A
        )

    def create_display(self) -> Display:
        return Display(self._width, self._height, self._hub)