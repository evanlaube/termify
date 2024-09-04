
from .element import Element

class Button(Element):
    def __init__(self, label, action, refreshFunction=None, color=-1, background=-1):
        super().__init__(label, refreshFunction=refreshFunction, color=color, background=background)
        self.action = action
        self.selectable = True

    def triggerAction(self):
        result = self.action()
        if result != None:
            self.label = result

    def getStr(self, selected=False):
        if selected:
            return '[*] ' + self.label
        else:
            return '[ ] ' + self.label

