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
        elementKey = list(self.elements)[self.selectedIndex]
        if key == curses.KEY_UP or key == ord('k'): 
            if self.selectedIndex <= 0:
                return
            self.selectedIndex -= 1
        elif key == curses.KEY_DOWN or key == ord('j'):
            if self.selectedIndex >= len(self.elements)-1:
                return
            self.selectedIndex += 1
        elif key == 10: # Enter/Return
            self.elements[elementKey].triggerAction()
        elif key == ord('q'):
            exit()
        else:
            self.elements[elementKey].handleInput(key)
            
            
    def update(self):
        for id, key in enumerate(self.elements.keys()):
            self.elements[key].update()
    
    def display(self, stdscr):
        stdscr.clear()
        for id, key in enumerate(self.elements.keys()):
            # TODO: Find some way to set color to colors of elements without using init_pair
            element = self.elements[key]
            selected = (id == self.selectedIndex)
            stdscr.addstr(str(element.getStr(selected=selected)) + '\n')
