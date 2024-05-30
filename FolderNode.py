import humanize

class FolderNode(object):        
    def __init__(self, name:str):
        self.name = name
        self.size = 0
        self.toRemove = False
    
    def getLabel(self) -> str:
        return self.name + ' - ' + humanize.naturalsize(self.size)
    
    def isDir(self) -> bool:
        return True
    
    def addToSize(self, size: int) -> None:
        self.size += size
        

        
