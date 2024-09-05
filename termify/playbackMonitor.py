
import threading
import time

class PlaybackMonitor:
    def __init__(self, api, updateInterval=0.2):
        self.api = api
        self.lock = threading.Lock()
        self.currentSong = {}
        self.updateInterval = updateInterval 

    def run(self):
        while True:
            song = self.fetchCurrentSong()

            if song == None:
                continue

            with self.lock:
                self.currentSong = song
            time.sleep(self.updateInterval)

    def fetchCurrentSong(self):
        return self.api.getCurrentSong()

    def start(self):
        thread = threading.Thread(target=self.run, daemon=True)
        thread.start()

    def getCurrentSong(self):
        with self.lock:
            return self.currentSong
