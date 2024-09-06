
from termify.spotifyApi import SpotifyApi
from termify.spotifyAppController import SpotifyAppController
from termify.ui import UIManager
from dotenv import set_key, get_key
import curses
import os
from pathlib import Path

envPath = Path(os.getenv('TERMIFY_ENV_PATH', Path.home() / '.termify' / '.env'))

def main():
    clientId = get_key(envPath, 'TFY_CLIENT_ID')
    
    if clientId == None:
        print("No Client ID found in .env file.")
        id = input("\tEnter your Spotify App Client Id: ")
        configDir = Path(os.getenv('TERMIFY_ENV_PATH', Path.home() / '.termify'))
        os.makedirs(str(configDir))
        set_key(envPath, 'TFY_CLIENT_ID', id)
    
    curses.wrapper(launch)

def launch(stdscr):
    api = SpotifyApi()
    uiManager = UIManager(stdscr, api)
    controller = SpotifyAppController(api, uiManager)

    controller.run()

if __name__ == '__main__':
    main()
