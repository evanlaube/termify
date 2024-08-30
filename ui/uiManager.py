import curses

class UIManager:
    def __init__(self, stdscr, api):
        self.stdscr = stdscr
        self.api = api
        self.currentMenu = None
        self.menus = {} 
        self.shouldExit = False

    def run(self):
        self.stdscr.clear()
        self.stdscr.refresh()
        self.mainLoop()

    def mainLoop(self):
        try:
            while self.shouldExit == False:
                if self.currentMenu != None:
                    self.menus[self.currentMenu].display(self.stdscr)
                key = self.stdscr.getch()
                self.menus[self.currentMenu].handleInput(key)
        except KeyboardInterrupt:
            self.shouldExit = False 


    #def displayMenu(self, menu):
    #    self.stdscr.clear()
    #    elements = self.menus[menu]['items']
    #    for id, element in enumerate(elements):
    #        if element['type'] == 'button':
    #            if id == self.selectedElement:
    #                self.stdscr.addstr('[*] ')
    #            else:
    #                self.stdscr.addstr('[ ] ')
    #            self.stdscr.addstr(element['label'] + '\n')

                
    def addMenu(self, menu):
        name = menu.name
        self.menus[name] = menu

    def switchMenu(self, menu):
        if menu in self.menus.keys():
            self.currentMenu = menu

    def executeAction(self, menu, itemId):
        item = self.menus[menu]['items'][itemId]

        action = item.get('action')
        if action:
            action()

