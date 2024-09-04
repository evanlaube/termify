import curses
import time

class UIManager:
    def __init__(self, stdscr, api):
        self.stdscr = stdscr
        self.api = api
        self.currentMenu = None
        self.menus = {} 
        self.shouldExit = False

        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, -1, -1)
        self.stdscr.bkgd(' ', curses.color_pair(1))
        self.stdscr.clear()
        self.stdscr.refresh()
        self.stdscr.timeout(1000)

    def run(self):
        self.stdscr.clear()
        self.stdscr.refresh()
        self.mainLoop()

    def mainLoop(self):
        try:
            while self.shouldExit == False:
                if self.currentMenu != None:
                    self.stdscr.clear()
                    self.menus[self.currentMenu].update()
                    self.menus[self.currentMenu].display(self.stdscr)
                key = self.stdscr.getch()
                self.menus[self.currentMenu].handleInput(key)
        except KeyboardInterrupt:
            self.shouldExit = False 

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

