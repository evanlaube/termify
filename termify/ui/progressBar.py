
from .element import Element

class ProgressBar(Element):
    def __init__(self, length, progress=0, refreshFunction=None, color=0, label=''):
        super().__init__(label, refreshFunction=refreshFunction, color=color)
        self.length = length
        self.selectable = False
        self.progress = progress # Float between 0 and 1

    def getStr(self, selected=False):
        active = round(self.progress*self.length)
        output = '●' * active + '○' * (self.length-active)
        return output
    
    def update(self):
        if self.refreshFunction == None:
            return

        try:
            self.progress = float(self.refreshFunction())
            if self.progress > 1:
                raise Exception("ProgressBar progress cannot be greater than 1")
            elif self.progress < 0:
                raise Exception("ProgressBar progress cannot be negative")
        except:
            raise Exception("Unable to run refreshFunction for progressbar")
