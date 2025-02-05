
from procyon import Button, Label, Menu, RowBar

class PlaylistSelector(Menu):
    """A menu for selecting which playlist to set playback to. The menu consists
    of a set of buttons corrosponding to each playlist saved or created by the
    user's spotify account
    """
    def __init__(self, controller):
        self.controller = controller
        self.api = controller.getApi()
        self.monitor = controller.getMonitor()

        super().__init__('playlistSelector')
        self.buildMenu()

    def _selectPlaylistButtonFunction(self, uri):
        """ The function to run when pressing a button corrosponding to a playlist
        :param uri: The playlist uri to play on pressing the button
        :type uri: str
        """
        try:
            currentSongData = self.monitor.getCurrentSong()

            prevUri = None
            try:
                prevUri = currentSongData['context']['uri']
                prevPlaylistId = prevUri.strip().split(':')[2]
                # Set button label for last rowbar to 'Play' instead of 'Playing'
                self.elements['playlist-' + prevPlaylistId].elements[1].label = "Play"
            except:
                # If unable to change button label, just reload all playlist rowbars
                self.api.play(contextURI=uri)
                self.elements = {}
                self.buildMenu()
                return

            self.api.play(contextURI=uri)
            
            newPlaylistId = uri.strip().split(':')[2]
            self.elements['playlist-'+newPlaylistId].elements[1].label = 'Currently Playing'

        except:
            errorMsg = "No active streaming device found. Before using termify to control spotify, ensure that there is an active instance running on your account."
            self.controller.displayError(errorMsg, 80, self)

    def createPlaylistRowbar(self, playlistJson):
        """ Create a visual rowbar to display playlist information and contain 
        action buttons
        :param playlistJson: The data for the playist from the Spotify API
        :type param: dict
        :return: The RowBar element
        :rtype: RowBar
        """

        # Format name to be at least 40 characters - padded with spaces
        name = f"{playlistJson['name'] : <40}"
        uri = playlistJson['uri']

        playButtonText = 'Play'

        currentSongData = self.monitor.getCurrentSong()

        if currentSongData is not None:
            if currentSongData.get('context', {}).get('uri', {}) == uri:
                playButtonText = 'Currently Playing'

        label = Label('\t' + name)
        playButton = Button(playButtonText, action=lambda: self._selectPlaylistButtonFunction(uri))
        bar = RowBar([label, playButton])
        
        return bar

    def buildMenu(self):
        """Initialize all elements and add them to the menu """
        self.addElement('prompt', Label("Select a playlist: "))
        playlists = self.api.getUserPlaylists()
        if playlists == {}:
            self.addElement('noPlaylistLabel', Label("You don't have any saved or created playlists!"))
        else:
            for playlist in playlists['items']:
                self.addElement('playlist-' + playlist['id'], self.createPlaylistRowbar(playlist))

        self.addElement('cancelButton', Button('Cancel', lambda: self.controller.loadMain()))
