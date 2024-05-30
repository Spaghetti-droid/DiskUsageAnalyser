class FSNode(object):        
    def __init__(self, name:str, size:int):
        self.name = name
        self.size = size
    
    def getLabel(self) -> str:
        return self.name + ' - ' + str(self.size)
    
    def isDir(self) -> bool:
        raise "Should not be called!"
    
    def addToSize(self, size: int) -> None:
        raise "Should not be called!"

class FileNode(FSNode):    
    def isDir(self) -> bool:
        return False

class FolderNode(FSNode):
    
    def __init__(self, name:str):
        super().__init__(name, 0)
    
    def isDir(self) -> bool:
        return True
    
    def addToSize(self, size: int) -> None:
        self.size += size
        

        
