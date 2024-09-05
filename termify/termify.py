
from termify.spotifyApi import SpotifyApi
from termify.spotifyAppController import SpotifyAppController
from termify.ui import UIManager
from dotenv import set_key, get_key
import curses


def main():
    clientId = get_key('.env', 'TFY_CLIENT_ID')
    
    if clientId == None:
        print("No Client ID found in .env file.")
        id = input("\tEnter your Spotify App Client Id: ")
        set_key('.env', 'TFY_CLIENT_ID', id)
    
    curses.wrapper(launch)

def launch(stdscr):
    api = SpotifyApi()
    uiManager = UIManager(stdscr, api)
    controller = SpotifyAppController(api, uiManager)

    controller.run()

main()
