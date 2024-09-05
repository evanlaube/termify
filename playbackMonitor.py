
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
            with self.lock:
                self.currentSong = self.fetchCurrentSong()
            time.sleep(self.updateInterval)

    def fetchCurrentSong(self):
        self.currentSong = self.api.getCurrentSong()

    def start(self):
        thread = threading.Thread(target=self.run, daemon=True)
        thread.start()

    def getCurrentSong(self):
        currentSong = None
        with self.lock:
            currentSong = self.currentSong
        return currentSong
