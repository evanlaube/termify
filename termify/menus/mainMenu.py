
from math import floor
from procyon import Button, Label, Menu, ProgressBar, RowBar, colors

from termify import __version__

class MainMenu(Menu):
    """ The main menu that displays plackback controls and information, as well
    as a set of buttons to access other features of the app.
    :param controller: The controller to access methods from
    :type controller: SpotifyAppController
    """
    def __init__(self, controller):
        self.controller = controller
        self.monitor = controller.getMonitor()
        self.api = controller.getApi()
        super().__init__('main')
        self._desiredVolume = self.monitor.getCurrentVolume()
        self._buildMenu()
    
    def _playPauseToggle(self):
        """Toggle playback between play and pause
        :return: The new label of the playback toggle button - either 'Play' or 'Pause'
        :rtype: str
        """
        state = self.api.getPlaybackState()

        if state.status_code == 204:
            self.controller.selectPlaybackDevice()
            return "Play"

        if(state.json()['is_playing']):
            self.api.pause()
            return 'Play'
        else:
            self.api.play()
            return 'Pause'

    def _getPlayButtonLabel(self):
        """Get what the label of the playback button should be. Makes a whole request to API
        :return: Label of playback toggle button - either 'Play' or 'Pause'
        :rtype: str
        """
        state = self.api.getPlaybackState()
    
        if(state.status_code == 200 and state.json()['is_playing']):
            return 'Pause'
        return 'Play'

    def _getCurrentSongDisplayLabel(self):
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

    def _songProgressBarRefresh(self) -> float:
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

    def _getSongTimeLabel(self):
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
    
    def _increaseVolume(self):
        """ Button function to increase playback volume by 10% """
        currentvolume = self._desiredVolume 
        newVolume = min(currentvolume + 10, 100)

        self._desiredVolume = newVolume
        self.api.setVolume(self._desiredVolume)

    def _decreaseVolume(self):
        """ Button function to decrease playback volume by 10% """
        currentVolume = self._desiredVolume 
        newVolume = max(currentVolume-10, 0)

        self._desiredVolume = newVolume
        self.api.setVolume(self._desiredVolume)

    def _volumeBarRefresh(self):
        """ Refresh function for volume progress bar """
        return self._desiredVolume / 100.0
    
    def _buildMenu(self):
        """Initialize all of the elements in the menu and add them to self """
        playButtonLabel = self._getPlayButtonLabel()

        self.addElement('currentSong', Label(str(self._getCurrentSongDisplayLabel()), refreshFunction=lambda: self._getCurrentSongDisplayLabel()))

        progressBar = ProgressBar(20, refreshFunction=lambda: self._songProgressBarRefresh())
        timeLabel = Label(str(self._getSongTimeLabel()), refreshFunction=lambda: self._getSongTimeLabel())
        progressBarRow = RowBar([Label(''), progressBar, timeLabel]) # Add empty label to indent rowBar
        self.addElement('progressBar', progressBarRow)
        self.addElement('postProgressbarBreak', Label('')) # Line break under progress bar

        volumeProgressBar = ProgressBar(10, refreshFunction=lambda: self._volumeBarRefresh())
        volumeUpButton = Button("+", lambda: self._increaseVolume())
        volumeDownButton = Button("-", lambda: self._decreaseVolume())

        volumeRowBar = RowBar([volumeDownButton, volumeProgressBar, volumeUpButton], separator=' ')
        self.addElement('volumeRowBar', volumeRowBar)

        playButton = Button(playButtonLabel, lambda: self._playPauseToggle(), setLabelToResult=True)
        skipButton = Button('Skip Song', lambda: self.api.skip())
        prevButton = Button('Previous Song', lambda: self.api.prev())
        playbackBar = RowBar([playButton, skipButton, prevButton])
        self.addElement('playbackControlBar', playbackBar)


