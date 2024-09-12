
import curses
from .element import Element

class RowBar(Element):
    """An element container for displaying multiple elements inline in a menu.
    :param elements: A list of Elements that will be added to the RowBar
    :type elements: list
    :param separator: The character(s) that will be printed between each element in the bar
    :type separator: str, optional
    """
    def __init__(self, elements, separator='\t', color=0,):
        """Constructor method
        """
        super().__init__('', color=color)
        self.selectable = True 
        self.isContainer = True
        self.elements = elements
        self.separator = separator
        self.selectedIndex = 0

        allNotSelectable = True
        for element in self.elements:
            if element.selectable:
                allNotSelectable = False
                break

        if allNotSelectable:
            self.selectable = False

    def handleInput(self, key):
        """Pass input keys from the menu to the selected element
        :param key: The key that was input
        :type key: int
        """
        if (key in (curses.KEY_LEFT, ord('h'))) and self.selectedIndex > 0:
            self.selectedIndex -= 1
        elif (key in (curses.KEY_RIGHT, ord('l'))) and self.selectedIndex < len(self.elements)-1:
            self.selectedIndex += 1

    def getStr(self, selected=False):
        """Get the display string of the rowbar, including getting the strings of all of 
        the elements contained inside the rowbar
        :param selected: Whether or not the bar is selected in the menu
        :type selected: bool
        :return: The text that the bar should be printed as
        :rtype: str
        """
        string = ''
        for id, element in enumerate(self.elements):
            if id == self.selectedIndex and selected:
                string += element.getStr(selected=True) + self.separator
            else:
                string += element.getStr() + self.separator

        return string

    def triggerAction(self):
        """Trigger the action of the element contained in the bar at the selected index"""
        self.elements[self.selectedIndex].triggerAction()

    def update(self):
        """Update each element in the RowBar"""
        for element in self.elements:
            element.update()
