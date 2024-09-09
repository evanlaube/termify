import curses


class Menu:
    def __init__(self, name):
        self.name = name
        self.elements = {} 
        self.selectedIndex = 0
        self.hasSelectable = False

    def addElement(self, name, element):
        if name in self.elements.keys():
            raise Exception(f"Element with name '{name}' already exists")
        self.elements[name] = element
        if element.selectable and self.hasSelectable == False:
            self.hasSelectable = True
            self.selectedIndex = len(self.elements)-1

    def handleInput(self, key):
        elementKey = list(self.elements)[self.selectedIndex]
        if key == curses.KEY_UP or key == ord('k'): 
            if self.selectedIndex <= 0:
                return
            self.decreaseSelectedIndex()
        elif key == curses.KEY_DOWN or key == ord('j'):
            if self.selectedIndex >= len(self.elements)-1:
                return
            self.increaseSelectedIndex()
        elif key == 10: # Enter/Return
            self.elements[elementKey].triggerAction()
        elif key == ord('q'):
            exit()
        else:
            self.elements[elementKey].handleInput(key)

    def increaseSelectedIndex(self):
        if self.selectedIndex >= len(self.elements)-1:
            return
        self.selectedIndex += 1
        while self.elements[list(self.elements)[self.selectedIndex]].selectable == False:
            self.increaseSelectedIndex()
            if(self.selectedIndex >= len(self.elements)-1):
                self.decreaseSelectedIndex()
                break

    def decreaseSelectedIndex(self):
        if self.selectedIndex <= 0:
            return
        self.selectedIndex -= 1
        while self.elements[list(self.elements)[self.selectedIndex]].selectable == False:
            self.decreaseSelectedIndex()
            if(self.selectedIndex <= 0):
                self.increaseSelectedIndex()
                break
            
            
    def update(self):
        for id, key in enumerate(self.elements.keys()):
            self.elements[key].update()
    
    def display(self, stdscr, ending='\n'):
        stdscr.clear()
        for id, key in enumerate(self.elements.keys()):
            element = self.elements[key]
            
            if element.isContainer:
                separator = element.separator
                for barid, e in enumerate(element.elements):
                    barselected = False
                    if barid == element.selectedIndex:
                        barselected = True
                    color = e.color

                    stdscr.addstr(str(e.getStr(selected=barselected)) + separator, curses.color_pair(color))
                stdscr.addstr('\n')
            else:
                color = element.color
                selected = (id == self.selectedIndex)

                stdscr.addstr(str(element.getStr(selected=selected)) + ending, curses.color_pair(color))
