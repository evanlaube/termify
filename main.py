
from spotifyApi import SpotifyApi
import curses

from ui import UIManager, Button, Menu

def main(stdscr):
    api = SpotifyApi()

    #mainMenuItems = [{'type': 'button', 'label': 'Play', 'action': lambda: api.play()},{'type': 'button', 'label': 'Pause', 'action': lambda: api.pause()}]

    menu = Menu('main')
    playButton = Button('Play', lambda: api.play())
    pauseButton = Button('Pause', lambda: api.pause())
    menu.addElement(playButton)
    menu.addElement(pauseButton)
    
    uiManager = UIManager(stdscr, api)
    uiManager.addMenu(menu)
    uiManager.switchMenu('main')
    uiManager.run()

curses.wrapper(main)
