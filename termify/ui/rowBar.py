
import curses
from .element import Element

class RowBar(Element):
    def __init__(self, elements, separator='\t', color=0,):
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
        if (key in (curses.KEY_LEFT, ord('h'))) and self.selectedIndex > 0:
            self.selectedIndex -= 1
        elif (key in (curses.KEY_RIGHT, ord('l'))) and self.selectedIndex < len(self.elements)-1:
            self.selectedIndex += 1

    def getStr(self, selected=False):
        string = ''
        for id, element in enumerate(self.elements):
            if id == self.selectedIndex and selected:
                string += element.getStr(selected=True) + self.separator
            else:
                string += element.getStr() + self.separator

        return string

    def triggerAction(self):
        self.elements[self.selectedIndex].triggerAction()

    def update(self):
        for element in self.elements:
            element.update()
