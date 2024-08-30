import curses

class UIManager:
    def __init__(self, stdscr, api):
        self.stdscr = stdscr
        self.api = api
        self.currentMenu = None
        self.menus = {}
        self.shouldExit = False
        self.selectedElement = 0

    def run(self):
        self.stdscr.clear()
        self.stdscr.refresh()
        self.mainLoop()

    def mainLoop(self):
        try:
            while self.shouldExit == False:
                if self.currentMenu != None:
                    self.displayMenu(self.currentMenu)
                key = self.stdscr.getch()
                self.handleKeypress(key)
        except KeyboardInterrupt:
            self.shouldExit = False 


    def displayMenu(self, menu):
        self.stdscr.clear()
        elements = self.menus[menu]['items']
        for id, element in enumerate(elements):
            if element['type'] == 'button':
                if id == self.selectedElement:
                    self.stdscr.addstr('[*] ')
                else:
                    self.stdscr.addstr('[ ] ')
                self.stdscr.addstr(element['label'] + '\n')

                
                

    def handleKeypress(self, key):
        if key == curses.KEY_UP or key == ord('k'):
            self.selectedElement -= 1
        elif key == curses.KEY_DOWN or key == ord('j'):
            self.selectedElement += 1
        elif key == 10:
            self.executeAction(self.currentMenu, self.selectedElement)

    def addMenu(self, name, items):
        self.menus[name] = {'items': items}

    def switchMenu(self, menu):
        if menu in self.menus.keys():
            self.currentMenu = menu
            self.displayMenu(self.currentMenu)

    def executeAction(self, menu, itemId):
        item = self.menus[menu]['items'][itemId]

        action = item.get('action')
        if action:
            action()

