import threading
import time

class SpotifyWrapper:
    def __init__(self, api):
        self.api = api
        self.lock = threading.Lock()
        self.currentSong = {}
        self.updateInterval = 5 

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

            labelString = f'Currently Playing:\n\t{songTitle}\n\t{artistString} - {album}\n' 

            return labelString 
