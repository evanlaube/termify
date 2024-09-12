
from .element import Element

class ProgressBar(Element):
    """An element that displays a number in a range as a horizontal bar. This is
    useful for things like progressbars and visually showing percentages
    :param length: The amount of characters the progress bar is in width
    :type length: int
    :param progress: The starting progress of the bar, ranging from 0-1
    :type progresse: float
    :param refreshFunction: The function to run to refresh the label of the element
    :type refreshFunction: function
    :param color: The color to draw the text of the element in
    :type color: int, optional
    :param label: The text to display on the progress bar 
    :type label: str
    """

    def __init__(self, length, progress=0, refreshFunction=None, color=0, label=''):
        """Constructor method
        """
        super().__init__(label, refreshFunction=refreshFunction, color=color)
        self.length = length
        self.selectable = False
        self.progress = progress # Float between 0 and 1

    def getStr(self, selected=False):
        """Get the string that the progressbar should display as
        :return: Display string
        :rtype: str
        """
        active = round(self.progress*self.length)
        output = '●' * active + '○' * (self.length-active)
        return output
    
    def update(self):
        """Call the refresh function of the progressbar, and set its progress to
        the result of the function
        """
        if self.refreshFunction == None:
            return

        try:
            self.progress = float(self.refreshFunction())
            if self.progress > 1:
                raise Exception("ProgressBar progress cannot be greater than 1")
            elif self.progress < 0:
                raise Exception("ProgressBar progress cannot be negative")
        except:
            raise Exception("Unable to run refreshFunction for progressbar")
