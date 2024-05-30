from pathlib import Path
import argparse
from treelib import Tree, Node
from FSNode import *


def main():
    args = initArgParser()
    initialRoot = Path(args.root)
    tree = Tree()
    rootNode = FolderNode(initialRoot.name)
    tree.create_node(rootNode.name,str(initialRoot),data=rootNode)
    for root, dirs, files in initialRoot.walk(on_error=print):
        for dir in dirs: 
            addFolderNode(tree, root / dir, FolderNode(dir))
        
        for file in files:
            fullPath = root / file
            fileSize = fullPath.stat().st_size
            addFileNode(tree, fullPath, FileNode(file, fileSize))  
            updateSizes(tree, fullPath, fileSize)
            
    setDirLabels(tree)    
    tree.save2file("graph.txt")

def initArgParser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="Disk Usage Analyser", description="Plots disk usage in a tree plot")
    parser.add_argument("root", help="The path to the root directory whose contents should be analysed")
    parser.add_argument("-d", "--depth", type=int, help="How deep should the tree be displayed")
    return parser.parse_args()


def addFileNode(tree: Tree, path: Path, node: FileNode) -> None:
    tree.create_node(node.getLabel(),str(path),data=node, parent=str(path.parent))
    
def addFolderNode(tree: Tree, path: Path, node: FolderNode) -> None:
    tree.create_node(node.name,str(path),data=node, parent=str(path.parent))
    
def updateSizes(tree: Tree, path: Path, size:int) -> None:
    node = tree.parent(str(path))
    if(node == None):
        return
    
    node.data.addToSize(size) 
    updateSizes(tree, path.parent, size)
    
def setDirLabels(tree:Tree) -> None:
    for nodeStr in tree.expand_tree(filter = lambda x: x.data.isDir()):
        node = tree.get_node(nodeStr)
        node.tag = node.data.getLabel()


if __name__ == "__main__":
    main()