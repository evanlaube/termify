
import curses
from procyon import Panel, UIManager, Menu, Button, Label, RowBar, ProgressBar, colors 
from termify import __version__
from termify.playbackMonitor import PlaybackMonitor
from termify.spotifyApi.spotifyApi import SpotifyApi
from termify.menus import MainMenu, PlaylistSelector, PlaybackDeviceSelector, ErrorMenu, SideBar

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

        left, right = self.uiManager.splitVertical()
        self._sideBar = left
        self._mainPanel = right

        self._sideBar.setSize(24, -1)

        self.monitor : PlaybackMonitor = PlaybackMonitor(self.api)
        
        self.monitor.start()

        self.buildMenus()
        self.loadMain()

    def run(self):
        """Begin the main loop of the UIManager"""
        self.uiManager.run()

    def loadMain(self):
        """ Set the main panel back to the main menu """
        mainMenu = self.uiManager.getMenuByName('main')
        self._mainPanel.loadMenu(mainMenu)
        sideBar = self.uiManager.getMenuByName('sidebar')
        self._sideBar.loadMenu(sideBar)

    def loadMenu(self, menuName : Menu | str):
        """ Load a given menu into the main panel """
        if isinstance(menuName, str):
            menu = self.uiManager.getMenuByName(menuName)
        else:
            menu = menuName

        if menu is not None:
            self.uiManager._rootPanel.loadMenu(menu)

    def getMonitor(self) -> PlaybackMonitor:
        """ Returns the controller's playback monitor """
        return self.monitor

    def getApi(self) -> SpotifyApi:
        """ Returns the controller's spotify api instance """
        return self.api

    def buildMenus(self):
        """Create all menus and add them to the UIManager"""
        mainMenu = MainMenu(self)
        self.uiManager.addMenu(mainMenu)
        sideBar = SideBar(self)
        self.uiManager.addMenu(sideBar)

    def playbackControls(self):
        main = self.uiManager.getMenuByName('main')
        self._mainPanel.loadMenu(main)
        self.uiManager.selectPanel(self._mainPanel)

    def selectPlaybackDevice(self):
        """Create a new menu to select which playback device to use"""
        selectMenu = PlaybackDeviceSelector(self)
        self.uiManager.addMenu(selectMenu)
        self._mainPanel.loadMenu(selectMenu)
        self.uiManager.selectPanel(self._mainPanel)

    def selectPlaylist(self):
        """Create a new menu to select which of the user's saved playlists to play"""
        playlistMenu = PlaylistSelector(self)
        self.uiManager.addMenu(playlistMenu)
        self._mainPanel.loadMenu(playlistMenu)
        self.uiManager.selectPanel(self._mainPanel)

    def displayError(self, errorMessage, maxWidth=80, returnMenu=None):
        """ Display an error dialog to the user
        :param errorMessage: The message to display to the user
        :type errorMessage: str
        :param maxWidth: The max width for each line of the error message to be
        :type maxWidth: int, optional 
        :param returnMenu: The menu to return to after exiting the error 
        :type returnMenu: procyon.Menu 
        """
        errorMenu = ErrorMenu(self, errorMessage, maxWidth=maxWidth, returnMenu=returnMenu)
        self.uiManager.addMenu(errorMenu)
        self._mainPanel.loadMenu(errorMenu)
        self.uiManager.selectPanel(self._mainPanel)

