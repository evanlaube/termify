
from spotifyApi import SpotifyApi
from spotifyWrapper import SpotifyWrapper
import curses

from ui import UIManager, Button, Menu, Label
from ui.rowBar import RowBar 

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
    mainMenu.addElement('currentSong', Label(str(wrapper.getCurrentSongLabel()), refreshFunction=lambda: wrapper.getCurrentSongLabel()))

    playButton = Button(playButtonLabel, lambda: playPauseToggle(api), setLabelToResult=True)
    skipButton = Button('Skip Song', lambda: api.skip())
    prevButton = Button('Previous Song', lambda: api.prev())
    playbackBar = RowBar([playButton, skipButton, prevButton])
    mainMenu.addElement('playbackBar', playbackBar)

    mainMenu.addElement('quitButton', Button('Quit', lambda: exit()))
    
    uiManager = UIManager(stdscr, api)
    uiManager.addMenu(mainMenu)
    uiManager.switchMenu('main')
    uiManager.run()

curses.wrapper(main)
