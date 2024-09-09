
from .element import Element

class Label(Element):
    def __init__(self, label, refreshFunction=None, color=0):
        super().__init__(label, refreshFunction=refreshFunction, color=color)

