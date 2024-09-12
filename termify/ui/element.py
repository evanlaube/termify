
class Element:
    """A parent class to base all UI elements off of. A base element draws similar
    to a label, but it is not recommended to insert a plain element into a menu
    :param label: The text to display on the element
    :type label: str
    :param refreshFunction: The function to run to refresh the label of the element
    :type refreshFunction: function
    :param color: The color to draw the text of the element in
    :type color: int, optional
    """
    def __init__(self, label, refreshFunction=None, color=0):
        """Constructor method
        """
        self.label = label
        self.color = color
        self.refreshFunction = refreshFunction
        self.selectable = False
        self.isContainer = False
    
    def update(self):
        """Update the label of the element by running its refreshFunction
        """
        if self.refreshFunction == None:
            return 

        try:
            self.label = self.refreshFunction()
        except:
            raise Exception("Unable to run refreshFunction for label:", self.label)
    
    def triggerAction(self):
        raise NotImplementedError("This method should be overwritten by subclasses")

    def getStr(self, selected=False):
        """Get the display string of the element
        :return: The text to display the element as
        :rtype: str
        """
        return self.label
    
    def handleInput(self, key):
        pass

