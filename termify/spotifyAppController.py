
import curses
from procyon import UIManager, Menu, Button, Label, RowBar, ProgressBar, colors 
from termify import __version__
from termify.playbackMonitor import PlaybackMonitor
from termify.spotifyApi.spotifyApi import SpotifyApi
from termify.menus import MainMenu, PlaylistSelector, PlaybackDeviceSelector
from math import floor

class SpotifyAppController:
    """A class that acts as a wrapper between the ui module and spotifyApi module. 
    The purpose of this class is to create all of the menus, as well as the functions
    that are needed by them
    :param api: The SpotifyApi to make requests with
    :type api: SpotifyApi
    :param uiManager: The UIManager to create menus inside of
    :type uiManager: UIManager"""
    def __init__(self, api : SpotifyApi, uiManager : UIManager):
        """Constructor method
        """
        self.api : SpotifyApi = api
        self.uiManager : UIManager = uiManager
        self.monitor : PlaybackMonitor = PlaybackMonitor(self.api)
        
        self.monitor.start()

        self.buildMenus()
        self.loadMain()

    def run(self):
        """Begin the main loop of the UIManager"""
        self.uiManager.run()

    def loadMain(self):
        mainMenu = self.uiManager.getMenuByName('main')
        self.uiManager._rootPanel.loadMenu(mainMenu)

    def getMonitor(self) -> PlaybackMonitor:
        return self.monitor

    def getApi(self) -> SpotifyApi:
        return self.api

    def buildMenus(self):
        """Create all menus and add them to the UIManager"""
        mainMenu = MainMenu(self)
        self.uiManager.addMenu(mainMenu)

    def selectPlaybackDevice(self):
        """Create a new menu to select which playback device to use"""
        selectMenu = PlaybackDeviceSelector(self)
        self.uiManager.addMenu(selectMenu)
        self.uiManager._rootPanel.loadMenu(selectMenu)

    def selectPlaylist(self):
        """Create a new menu to select which of the user's saved playlists to play"""
        playlistMenu = PlaylistSelector(self)
        self.uiManager.addMenu(playlistMenu)
        self.uiManager._rootPanel.loadMenu(playlistMenu)

