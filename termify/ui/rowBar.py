
import curses
from .element import Element

class RowBar(Element):
    def __init__(self, elements, seperator='\t', color=-1, background=-1):
        super().__init__('', color=color, background=background)
        self.selectable = True 
        self.elements = elements
        self.seperator = '\t'
        self.selectedIndex = 0

    def handleInput(self, key):
        if (key in (curses.KEY_LEFT, ord('h'))) and self.selectedIndex > 0:
            self.selectedIndex -= 1
        elif (key in (curses.KEY_RIGHT, ord('l'))) and self.selectedIndex < len(self.elements)-1:
            self.selectedIndex += 1

    def getStr(self, selected=False):
        string = ''
        for id, element in enumerate(self.elements):
            if id == self.selectedIndex and selected:
                string += element.getStr(selected=True) + self.seperator
            else:
                string += element.getStr() + self.seperator

        return string

    def triggerAction(self):
        self.elements[self.selectedIndex].triggerAction()
