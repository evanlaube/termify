
import curses
from termify.playbackMonitor import PlaybackMonitor
from termify.spotifyApi.spotifyApi import SpotifyApi
from termify.ui import UIManager, Menu, Button, Label, RowBar, ProgressBar, colors 
from math import floor


class SpotifyAppController:
    """A class that acts as a wrapper between the ui module and spotifyApi module. 
    The purpose of this class is to create all of the menus, as well as the functions
    that are needed by them
    :param api: The SpotifyApi to make requests with
    :type api: SpotifyApi
    :param uiManager: The UIManager to create menus inside of
    :type uiManager: UIManager"""
    def __init__(self, api, uiManager):
        """Constructor method
        """
        self.api = api
        self.uiManager = uiManager
        self.monitor = PlaybackMonitor(self.api)
        
        self.monitor.start()

        self.buildMenus()
        self.uiManager.switchMenu('main')

    def run(self):
        """Begin the main loop of the UIManager"""
        self.uiManager.run()

    
    def playPauseToggle(self):
        """Toggle playback between play and pause
        :return: The new label of the playback toggle button - either 'Play' or 'Pause'
        :rtype: str
        """
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
        """Get what the label of the playback button should be. Makes a whole request to API
        :return: Label of playback toggle button - either 'Play' or 'Pause'
        :rtype: str
        """
        state = self.api.getPlaybackState()
    
        if(state.status_code == 200 and state.json()['is_playing']):
            return 'Pause'
        return 'Play'

    def getCurrentSongDisplayLabel(self):
        """Get the formatted string of all of the information to display about
        the currently playing song
        :return: Formatted string of song information
        :rtype: str
        """
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
        """Refresh function for the song progress bar
        :return: The percentage of progress through current song - between 0 and 1
        :rtype: float
        """
        currentSong = self.monitor.getCurrentSong()
        if currentSong == None or currentSong == {}:
            return 0

        songLength = float(currentSong['item']['duration_ms'])
        progress = float(currentSong['progress_ms'])

        if progress > songLength:
            progress = songLength

        return progress / songLength 

    def getSongTimeLabel(self):
        """Gets the numerical label of the progress through the song
        :return: Numerical progress label
        :rtype: str
        """
        currentSong = self.monitor.getCurrentSong()
        if currentSong == None or currentSong == {}:
            return "(-:-- / -:--)" 

        songLength = floor(currentSong['item']['duration_ms'] / 1000.0)
        progress = floor(currentSong['progress_ms'] / 1000.0)
        if progress > songLength:
            progress = songLength

        return f'({progress//60}:{(progress%60):02d} / {songLength//60}:{(songLength%60):02d})'

        
    def buildMenus(self):
        """Create all menus and add them to the UIManager"""
        self.buildMainMenu()

    def buildMainMenu(self):
        """Insert the main menu with basic playback control, as well as access to switching to other menus, 
        into the UIManager"""
        mainMenu = Menu('main')
        playButtonLabel = self.getPlayButtonLabel()

        mainMenu.addElement('titleBar', Label("Termify v1.1.1\n", color=colors.CYAN))
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

        mainMenu.addElement('changePlaylistButton', Button('Select a Playlist', lambda: self.selectPlaylist()))
        mainMenu.addElement('changeDeviceButton', Button('Change Playback Device', lambda: self.selectPlaybackDevice()))
        mainMenu.addElement('quitButton', Button('Quit', lambda: exit()))
        
        self.uiManager.addMenu(mainMenu)

    def selectPlaybackDevice(self):
        """Create a new menu to select which playback device to use"""
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

    def createPlaylistRowbar(self, playlistJson):
        """ Create a visual rowbar to display playlist information and contain 
        action buttons
        :param playlistJson: The data for the playist from the Spotify API
        :type param: dict
        :return: The RowBar element
        :rtype: RowBar"""
        # Format name to be at least 40 characters - padded with spaces
        name = f"{playlistJson['name'] : <40}"
        uri = playlistJson['uri']

        label = Label('\t' + name)
        playButton = Button('Play', action=lambda: self.api.play(contextURI=uri))
        bar = RowBar([label, playButton])
        
        return bar

    
    def selectPlaylist(self):
        """Create a new menu to select which of the user's saved playlists to play"""
    
        prevMenu = self.uiManager.currentMenu

        playlistMenu = Menu("playlistSelect")

        playlistMenu.addElement('prompt', Label("Select a playlist: "))

        playlists = self.api.getUserPlaylists()
        if playlists == {}:
            playlistMenu.addElement('noPlaylistLabel', Label("You don't have any saved or created playlists!"))
        else:
            for playlist in playlists['items']:
                playlistMenu.addElement('playlist-'+playlist['id'], self.createPlaylistRowbar(playlist))

        playlistMenu.addElement('cancelButton', Button('Cancel', lambda: self.uiManager.switchMenu(prevMenu)))

        self.uiManager.addMenu(playlistMenu)
        self.uiManager.switchMenu('playlistSelect')



