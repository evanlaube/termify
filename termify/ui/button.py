
from .element import Element

class Button(Element):
    def __init__(self, label, action, refreshFunction=None, color=-1, background=-1, setLabelToResult=False):
        super().__init__(label, refreshFunction=refreshFunction, color=color, background=background)
        self.action = action
        self.selectable = True
        self.setLabelToResult = setLabelToResult

    def triggerAction(self):
        result = self.action()
        if type(result) == str and self.setLabelToResult:
            self.label = str(result)

    def getStr(self, selected=False):
        if selected:
            return '[>' + self.label + '<]'
        else:
            return '[ ' + self.label + ' ]'

