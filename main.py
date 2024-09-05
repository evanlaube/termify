
from spotifyApi import SpotifyApi
from spotifyAppController import SpotifyAppController
from dotenv import set_key, get_key
import curses

from ui import UIManager

def main(stdscr):

    clientId = get_key('.env', 'TFY_CLIENT_ID')
    
    if clientId == None:
        print("No Client ID found in .env file.")
        id = input("\tEnter your Spotify App Client Id: ")
        set_key('.env', 'TFY_CLIENT_ID', id)
        curses.wrapper(main)
        return

    api = SpotifyApi()
    uiManager = UIManager(stdscr, api)
    controller = SpotifyAppController(api, uiManager)

    controller.run()


main(None)
