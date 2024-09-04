
import curses


class Menu:
    def __init__(self, name):
        self.name = name
        self.elements = {} 
        self.selectedIndex = 0 

    def addElement(self, name, element):
        if name in self.elements.keys():
            raise Exception(f"Element with name '{name}' already exists")
        self.elements[name] = element

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
            elementKey = list(self.elements)[self.selectedIndex]
            self.elements[elementKey].triggerAction()
        elif key == ord('q'):
            exit()
            
    
    def display(self, stdscr):
        stdscr.clear()
        for id, key in enumerate(self.elements.keys()):
            element = self.elements[key]
            selected = (id == self.selectedIndex)
            stdscr.addstr(element.getStr(selected=selected) + '\n')
