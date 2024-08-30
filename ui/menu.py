
import curses


class Menu:
    def __init__(self, name):
        self.name = name
        self.elements = []
        self.selectedIndex = 0 

    def addElement(self, element):
        self.elements.append(element)

    def handleInput(self, key):
        if key == curses.KEY_UP or key == ord('k'): 
            if self.selectedIndex <= 0:
                return
            self.selectedIndex -= 1
        elif key == curses.KEY_DOWN or key == ord('j'):
            if self.selectedIndex >= len(self.elements)-1:
                return
            self.selectedIndex += 1
        elif key == 10: # Enter/Return
            self.elements[self.selectedIndex].triggerAction()
            
    
    def display(self, stdscr):
        stdscr.clear()
        for id, element in enumerate(self.elements):
            selected = (id == self.selectedIndex)
            stdscr.addstr(element.getStr(selected=selected) + '\n')
