import humanize

class FolderNode(object):  
    """ Holds individual folder data for the tree
    """      
    def __init__(self, name:str):
        self.name = name
        self.size = 0
        self.toRemove = False
    
    def generateLabel(self) -> str:
        """Use name and size to create a formatted label

        Returns:
            str: Label displaying name and size
        """
        return self.name + ' - ' + humanize.naturalsize(self.size)
    
    def addToSize(self, size: int) -> None:
        """ Update self.size by adding size to it

        Args:
            size (int):
        """
        self.size += size
        

        
