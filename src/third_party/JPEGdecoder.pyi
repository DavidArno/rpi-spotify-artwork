from typing import Any
from third_party.decoder_types import FilePath, PixelRenderer, RGBColour, XYP

def jpeg(source:bytes|FilePath, callback:PixelRenderer, quality:int = 8, cache:bool=False) -> JPEGRenderer: ...

class JPEGRenderer():
    def __init__(self): ...

    def getMeta(self) -> 'XYP': ...

    def checkAndRender(
        self, 
        check_width:bool = False, 
        check_height:bool = False, 
        check_width_and_height:bool = False,
        x:int = 0, 
        y:int = 0, 
        placeholder = False, 
        phcolor:RGBColour = RGBColour(0xBBBBBB)) -> Any: ...

    def render(
        self, 
        x:int=0, 
        y:int=0, 
        placeholder:bool = False, 
        phcolor:RGBColour = RGBColour(0xBBBBBB)) -> Any: ...
