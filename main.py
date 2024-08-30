
from spotifyApi import SpotifyApi
import curses

from ui import UIManager

def main(stdscr):
    api = SpotifyApi()

    mainMenuItems = [{'type': 'button', 'label': 'Play', 'action': lambda: api.play()},{'type': 'button', 'label': 'Pause', 'action': lambda: api.pause()}]

    
    uiManager = UIManager(stdscr, api)
    uiManager.addMenu('mainMenu', mainMenuItems)
    uiManager.switchMenu('mainMenu')
    uiManager.run()

curses.wrapper(main)
