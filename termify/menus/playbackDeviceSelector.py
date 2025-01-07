
from procyon import Button, Label, Menu

from termify.playbackMonitor import PlaybackMonitor
from termify.spotifyApi.spotifyApi import SpotifyApi


class PlaybackDeviceSelector(Menu):
    """A menu that allows for a playback device to be selected. The menu consits
    of a set of buttons for each device that is available at a given time.
    :param controller: The controller to access methods from
    :type controller: SpotifyAppController"""
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
            self.addElement(buttonName, Button(name, lambda id=id: self._buttonFunc(id)))

        self.addElement('newLine', Label(''))
        self.addElement('cancelButton', Button('Cancel', lambda: self.controller.loadMain())) 
        self.addElement('deviceTip', Label("\nIf you don't see your device, make sure the Spotify app is running on it"))

    def _buttonFunc(self, id):
        try:
            self.api.setPlaybackDevice(id)
            self.controller.loadMain()
        except:
            errorMsg="Unable to switch playback device. Make sure that the selected device has an active instance of spotify running on it."
            self.controller.displayError(errorMsg, returnMenu=self)


