
class Element:
    def __init__(self, label, refreshFunction=None, color=-1, background=-1):
        self.label = label
        self.color = color
        self.background = background
        self.refreshFunction = refreshFunction
        self.selectable = False
    
    def update(self):
        if self.refreshFunction == None:
            return 

        try:
            self.label = self.refreshFunction()
        except:
            raise Exception("Unable to run refreshFunction for label:", self.label)
    
    def triggerAction(self):
        raise NotImplementedError("This method should be overwritten by subclasses")

    def getStr(self, selected=False):
        return self.label

