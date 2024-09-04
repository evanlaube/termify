
from spotifyApi import SpotifyApi
from spotifyWrapper import SpotifyWrapper
import curses

from ui import UIManager, Button, Menu, Label 

def playPauseToggle(api):
    state = api.getPlaybackState()

    if(state.json()['is_playing']):
        api.pause()
        return 'Play'
    else:
        api.play()
        return 'Pause'

def getPlayButtonLabel(api):
    state = api.getPlaybackState()

    if(state.status_code == 200 and state.json()['is_playing']):
        return 'Pause'
    else:
        return 'Play'

def main(stdscr):
    api = SpotifyApi()
    wrapper = SpotifyWrapper(api)
    wrapper.start()

    mainMenu = Menu('main')
    playButtonLabel = getPlayButtonLabel(api)
    mainMenu.addElement('titleBar', Label("Termify v0.0.0\n", background=curses.COLOR_BLUE, color=curses.COLOR_WHITE))
    mainMenu.addElement('labelUpdate', Label(str(wrapper.getCurrentSongLabel()), refreshFunction=lambda: wrapper.getCurrentSongLabel()))
    mainMenu.addElement('playButton', Button(playButtonLabel, lambda: playPauseToggle(api), setLabelToResult=True))
    mainMenu.addElement('skipButton', Button('Skip Song', lambda: api.skip()))
    mainMenu.addElement('prevButton', Button('Previous Song', lambda: api.prev()))
    mainMenu.addElement('quitButton', Button('Quit', lambda: exit()))
    
    uiManager = UIManager(stdscr, api)
    uiManager.addMenu(mainMenu)
    uiManager.switchMenu('main')
    uiManager.run()

curses.wrapper(main)
