
from procyon import Button, Label, Menu

from termify.playbackMonitor import PlaybackMonitor
from termify.spotifyApi.spotifyApi import SpotifyApi


class PlaybackDeviceSelector(Menu):
    def __init__(self, controller):
        self.controller = controller
        self.api: SpotifyApi = controller.getApi()
        self.monitor: PlaybackMonitor = controller.getMonitor()

        super().__init__('playbackDeviceSelector')
        self.buildMenu()

    def buildMenu(self): 
        devices = self.api.getDevices()['devices']
        self.addElement('prompt', Label('\nChoose a playback device: \n'))

        for device in devices:
            id = device['id']
            name = device['name']
            
            buttonName = 'select-' + id
            self.addElement(buttonName, Button(name, lambda id=id: (self.api.setPlaybackDevice(id), lambda: self.controller.loadMain())))

        self.addElement('newLine', Label(''))
        self.addElement('cancelButton', Button('Cancel', lambda: self.controller.loadMain())) 
        self.addElement('deviceTip', Label("\nIf you don't see your device, make sure the Spotify app is running on it"))

