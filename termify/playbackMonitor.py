
import threading
import time

class PlaybackMonitor:
    """A class that creates a new thread to be constantly checking the current status
    of the playback. 
    :param api: The SpotifyApi to access the playback information from
    :type api: SpotifyApi
    :param updateInterval: The number of seconds to wait before updating playback information
    :type updateInterval: float, optional
    """
    def __init__(self, api, updateInterval=0.2):
        self.api = api
        self.lock = threading.Lock()
        self.currentSong = {}
        self.updateInterval = updateInterval 

    def run(self):
        """Continuously check playback information"""
        while True:
            song = self.api.getPlaybackState().json()
            if song == None:
                continue

            with self.lock:
                self.currentSong = song
            time.sleep(self.updateInterval)

    def start(self):
        """Begin the run loop"""
        # First, get base data:
        song = self.api.getPlaybackState()
        if song is not None:
            try:
                self.currentSong = song.json()
            except:
                pass

        thread = threading.Thread(target=self.run, daemon=True)
        thread.start()

    def getCurrentSong(self):
        """Get the most up to date current song information
        :return: Current playback information
        :rtype: dict
        """
        try:
            with self.lock:
                if self.currentSong['item'] is None:
                    return None 

                return self.currentSong
        except:
            return None 

    def getCurrentVolume(self):
        """ Returns the current volume level of the playback """
        try:
            with self.lock:
                if self.currentSong['item'] is None:
                    return 0

                return self.currentSong['device']['volume_percent']
        except Exception as e:
            return 0
