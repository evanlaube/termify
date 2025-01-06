
from procyon import Button, Label, Menu, RowBar

class PlaylistSelector(Menu):
    def __init__(self, controller):
        self.controller = controller
        self.api = controller.getApi()
        self.monitor = controller.getMonitor()

        super().__init__('playlistSelector')
        self.buildMenu()

    def _selectPlaylistButtonFunction(self, uri):
        try:
            self.api.play(contextURI=uri)
        except Exception as e:
            # For now just return to prev menu
            # TODO: Find a clean way to notify the user to activate a streaming device
            return

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

        playButtonText = 'Play'

        currentSongData = self.monitor.getCurrentSong()
        
        try:
            if currentSongData['context']['uri'] == uri:
                playButtonText = 'Currently playing'
        except:
            #TODO: Clean up messy try/except
            playButtonText = 'Play'
    
        label = Label('\t' + name)
        playButton = Button(playButtonText, action=lambda: self._selectPlaylistButtonFunction(uri))
        bar = RowBar([label, playButton])
        
        return bar

    def buildMenu(self):
        self.addElement('prompt', Label("Select a playlist: "))
        playlists = self.api.getUserPlaylists()
        if playlists == {}:
            self.addElement('noPlaylistLabel', Label("You don't have any saved or created playlists!"))
        else:
            for playlist in playlists['items']:
                self.addElement('playlist-' + playlist['id'], self.createPlaylistRowbar(playlist))

        self.addElement('cancelButton', Button('Cancel', lambda: self.controller.loadMain()))
