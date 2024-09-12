import curses

class Menu:
    """A class for storing different 'screens' of elements, as well as handling input on 
    these screens. The main purpose of this class is to easily switch between menus using
    the UIManager class
    :param name: The name of the menu
    :type name: str
    """
    def __init__(self, name):
        """Constructor method
        """
        self.name = name
        self.elements = {} 
        self.selectedIndex = 0
        self.hasSelectable = False

    def addElement(self, name, element):
        """Add an element to the menu
        :param name: The name of the element
        :type name: str
        :param element: The element to add
        :type element: ui.Element
        """
        if name in self.elements.keys():
            raise Exception(f"Element with name '{name}' already exists")
        self.elements[name] = element
        if element.selectable and self.hasSelectable == False:
            self.hasSelectable = True
            self.selectedIndex = len(self.elements)-1

    def handleInput(self, key):
        """Forward the input key to the selected element in the menu
        :param key: The input key
        :type key: int
        """
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
        """Increase the selected index of the menu, skipping unselectable elements"""
        if self.selectedIndex >= len(self.elements)-1:
            return
        self.selectedIndex += 1
        while self.elements[list(self.elements)[self.selectedIndex]].selectable == False:
            self.increaseSelectedIndex()
            if(self.selectedIndex >= len(self.elements)-1):
                self.decreaseSelectedIndex()
                break

    def decreaseSelectedIndex(self):
        """Decrease the selected index of the menu, skipping unselectable elements"""
        if self.selectedIndex <= 0:
            return
        self.selectedIndex -= 1
        while self.elements[list(self.elements)[self.selectedIndex]].selectable == False:
            self.decreaseSelectedIndex()
            if(self.selectedIndex <= 0):
                self.increaseSelectedIndex()
                break
            
            
    def update(self):
        """Run the update function of each element in the menu"""
        for key in self.elements.keys():
            self.elements[key].update()
    
    def display(self, stdscr, ending='\n'):
        """Display all of the elements in the menu
        :param stdscr: The display to print to
        :param ending: The character(s) to print after each element
        :type ending: str
        """
        stdscr.clear()
        for id, key in enumerate(self.elements.keys()):
            element = self.elements[key]
            selected = (id == self.selectedIndex)
            
            if element.isContainer:
                separator = element.separator
                for barid, e in enumerate(element.elements):
                    barselected = False
                    if barid == element.selectedIndex:
                        barselected = True
                    color = e.color

                    stdscr.addstr(str(e.getStr(selected=(barselected & selected))) + separator, curses.color_pair(color))
                stdscr.addstr('\n')
            else:
                color = element.color
                stdscr.addstr(str(element.getStr(selected=selected)) + ending, curses.color_pair(color))
