
class Element:
    def __init__(self, label):
        self.label = label

    def triggerAction(self):
        raise NotImplementedError("This method should be overwritten by subclasses")

    def getStr(self, selected=False):
        return self.label
