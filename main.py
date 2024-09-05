
from spotifyApi import SpotifyApi
from spotifyAppController import SpotifyAppController
import curses

from ui import UIManager

def main(stdscr):
    api = SpotifyApi()
    uiManager = UIManager(stdscr, api)
    controller = SpotifyAppController(api, uiManager)

    controller.run()


curses.wrapper(main)
