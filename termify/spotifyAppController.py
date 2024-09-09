
import curses
from termify.playbackMonitor import PlaybackMonitor
from termify.spotifyApi.spotifyApi import SpotifyApi
from termify.ui import UIManager, Menu, Button, Label, RowBar, ProgressBar, colors
from math import floor


class SpotifyAppController:
    def __init__(self, api, uiManager):
        self.api = api
        self.uiManager = uiManager
        self.monitor = PlaybackMonitor(self.api)
        
        self.monitor.start()

        self.buildMenus()
        self.uiManager.switchMenu('main')

    def run(self):
        self.uiManager.run()

    
    def playPauseToggle(self):
        state = self.api.getPlaybackState()

        if state.status_code == 204:
            self.selectPlaybackDevice()
            return "Play"

        if(state.json()['is_playing']):
            self.api.pause()
            return 'Play'
        else:
            self.api.play()
            return 'Pause'
        
    def getPlayButtonLabel(self):
        state = self.api.getPlaybackState()
    
        if(state.status_code == 200 and state.json()['is_playing']):
            return 'Pause'
        return 'Play'

    def getCurrentSongDisplayLabel(self):
        currentSong = self.monitor.getCurrentSong()
        if currentSong == None or currentSong == {}:
            return "No media currently playing\n"

        songTitle = currentSong['item']['name']
        album = currentSong['item']['album']['name']
        artistString = '' 
        for artist in currentSong['item']['artists']:
            if artistString != '':
                artistString += ', '
            artistString += artist['name']


        labelString = f'Currently Playing:\n\t{songTitle}\n\t{artistString} - {album}\n' 

        return labelString 
    
    def songProgressBarRefresh(self):
        currentSong = self.monitor.getCurrentSong()
        if currentSong == None or currentSong == {}:
            return 0

        songLength = float(currentSong['item']['duration_ms'])
        progress = float(currentSong['progress_ms'])

        if progress > songLength:
            progress = songLength

        return progress / songLength 

    def getSongTimeLabel(self):
        currentSong = self.monitor.getCurrentSong()
        if currentSong == None or currentSong == {}:
            return "(-:-- / -:--)" 

        songLength = floor(currentSong['item']['duration_ms'] / 1000.0)
        progress = floor(currentSong['progress_ms'] / 1000.0)
        if progress > songLength:
            progress = songLength

        return f'({progress//60}:{(progress%60):02d} / {songLength//60}:{(songLength%60):02d})'

        
    def buildMenus(self):
        self.buildMainMenu()

    def buildMainMenu(self):
        mainMenu = Menu('main')
        playButtonLabel = self.getPlayButtonLabel()

        mainMenu.addElement('titleBar', Label("Termify v1.1.0\n", color=colors.CYAN))
        mainMenu.addElement('currentSong', Label(str(self.getCurrentSongDisplayLabel()), refreshFunction=lambda: self.getCurrentSongDisplayLabel()))

        progressBar = ProgressBar(20, refreshFunction=lambda: self.songProgressBarRefresh())
        timeLabel = Label(str(self.getSongTimeLabel()), refreshFunction=lambda: self.getSongTimeLabel())
        progressBarRow = RowBar([Label(''), progressBar, timeLabel]) # Add empty label to indent rowBar
        mainMenu.addElement('progressBar', progressBarRow)
        mainMenu.addElement('postProgressbarBreak', Label('')) # Line break under progress bar

        playButton = Button(playButtonLabel, lambda: self.playPauseToggle(), setLabelToResult=True)
        skipButton = Button('Skip Song', lambda: self.api.skip())
        prevButton = Button('Previous Song', lambda: self.api.prev())
        playbackBar = RowBar([playButton, skipButton, prevButton])
        mainMenu.addElement('playbackControlBar', playbackBar)

        mainMenu.addElement('changeDeviceButton', Button('Change Playback Device', lambda: self.selectPlaybackDevice()))
        mainMenu.addElement('quitButton', Button('Quit', lambda: exit()))
        
        self.uiManager.addMenu(mainMenu)

    def selectPlaybackDevice(self):
        prevMenu = self.uiManager.currentMenu 
        selectMenu = Menu('deviceSelect')

        devices = self.api.getDevices()['devices']
        selectMenu.addElement('prompt', Label('\nChoose a playback device: \n'))

        for device in devices:
            id = device['id']
            name = device['name']
            
            buttonName = 'select-' + id
            selectMenu.addElement(buttonName, Button(name, lambda id=id: (self.api.setPlaybackDevice(id), self.uiManager.switchMenu(prevMenu))))

        selectMenu.addElement('newLine', Label(''))
        selectMenu.addElement('cancelButton', Button('Cancel', lambda: self.uiManager.switchMenu(prevMenu)))
        selectMenu.addElement('deviceTip', Label("\nIf you don't see your device, make sure the Spotify app is running on it"))

        self.uiManager.addMenu(selectMenu)
        self.uiManager.switchMenu('deviceSelect')



