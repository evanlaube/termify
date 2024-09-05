import threading
import time
from math import floor

class SpotifyWrapper:
    def __init__(self, api):
        self.api = api
        self.lock = threading.Lock()
        self.currentSong = {}
        self.updateInterval = 0.2 

    def updateSong(self):
        while True:
            with self.lock:
                self.currentSong = self.fetchCurrentSong()
            time.sleep(self.updateInterval)

    def fetchCurrentSong(self):
        self.currentSong = self.api.getCurrentSong()
        return self.currentSong

    
    def start(self):
        thread = threading.Thread(target=self.updateSong, daemon=True)
        thread.start()

    def getCurrentSongLabel(self): 
        with self.lock:
            songTitle = self.currentSong['item']['name']
            album = self.currentSong['item']['album']['name']
            artistString = '' 
            for artist in self.currentSong['item']['artists']:
                if artistString != '':
                    artistString += ', '
                artistString += artist['name']

            songLength = floor(self.currentSong['item']['duration_ms'] / 1000.0)
            progress = floor(self.currentSong['progress_ms'] / 1000.0)
            if progress > songLength:
                progress = songLength

            labelString = f'Currently Playing:\n\t{songTitle}\t({progress//60}:{(progress%60):02d} / {songLength//60}:{(songLength%60):02d})\n\t{artistString} - {album}\n' 

            return labelString 
