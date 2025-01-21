
from termify import __version__
from procyon import Button, colors, Menu, Label

class SideBar(Menu):
    def __init__(self, controller):
        self.controller = controller
        self.monitor = controller.getMonitor()
        self.api = controller.getApi()

        super().__init__('sidebar')

        self._buildMenu()

    def _buildMenu(self):
        self.addElement('titleBar', Label(f"Termify {__version__}\n", color=colors.CYAN))
        self.addElement('playbackControllerButton', Button('Playback Controls', lambda: self.controller.playbackControls()))
        self.addElement('changePlaylistButton', Button('Select a Playlist', lambda: self.controller.selectPlaylist()))
        self.addElement('changeDeviceButton', Button('Change Device', lambda: self.controller.selectPlaybackDevice()))
        self.addElement('quitButton', Button('Quit', lambda: exit()))
