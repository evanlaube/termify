
from .element import Element

class Button(Element):
    def __init__(self, label, action):
        super().__init__(label)
        self.action = action

    def triggerAction(self):
        result = self.action()
        if result is not None:
            self.label = result

    def getStr(self, selected=False):
        if selected:
            return '[*] ' + self.label
        else:
            return '[ ] ' + self.label

