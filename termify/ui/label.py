
from .element import Element

class Label(Element):
    """A basic element type that simply displays text to the UI with no interactability
    :param label: The text to display on the label 
    :type label: str
    :param refreshFunction: The function to run to refresh the text of the label 
    :type refreshFunction: function
    :param color: The color to draw the text of the label in
    :type color: int, optional
    """
    def __init__(self, label, refreshFunction=None, color=0):
        """Constructor method
        """
        super().__init__(label, refreshFunction=refreshFunction, color=color)

