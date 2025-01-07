
from io import StringIO
from procyon import Button, Label, Menu, colors

class ErrorMenu(Menu):
    """A menu for displaying an error message to the user. The menu only has
    a space for an error message as well as a button to return to the desired menu.
    :param controller: The controller to access methods from
    :type controller: SpotifyAppController
    :param errorMessage: The error message that is displayed to the user
    :type errorMessage: str
    :param returnMenu: The menu to go back to upon pressing close button
    :type returnMenu: procyon.Menu
    """
    def __init__(self, controller, errorMessage, maxWidth=80, returnMenu=None):
        self.controller = controller
        self.errorMessage : str = errorMessage
        self.maxWidth : int = maxWidth 
        self.returnMenu : Menu | None = returnMenu

        super().__init__('errorMenu')
        self._buildMenu()

    def _buildMenu(self):
        """Initialize all of the elements in the menu and add them to self"""
        headerText = "\nAn Error Occurred\n"
        header = Label(headerText, color=colors.RED)
        self.addElement('header', header)

        bodyStrings = []
        head = 0  
        tail = 0
        while head < len(self.errorMessage):
            head = min(tail+self.maxWidth-4, len(self.errorMessage))

            if head != len(self.errorMessage):
                while head > tail and self.errorMessage[head-1] != ' ':
                    head -= 1

            if head == tail:
                head = min(tail+self.maxWidth-4, len(self.errorMessage))

            bodyStrings.append(self.errorMessage[tail:head].strip())
            tail = head

        for id, line in enumerate(bodyStrings):
            lineLabel = Label('\t' + line)
            self.addElement('body' + str(id), lineLabel)

        spacer = Label('')
        self.addElement('spacer', spacer)

        if self.returnMenu == None:
            closeFunc = lambda: self.controller.loadMain()
        else:
            closeFunc = lambda: self.controller.loadMenu(self.returnMenu)

        closeButton = Button('Close', closeFunc)
        self.addElement('closeButton', closeButton)

