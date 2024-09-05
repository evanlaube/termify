
from .element import Element

class Label(Element):
    def __init__(self, label, refreshFunction=None, color=-1, background=-1):
        super().__init__(label, refreshFunction=refreshFunction, color=color, background=background)

