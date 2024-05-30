from pathlib import Path
import argparse
from treelib import Tree
from FolderNode import *

# TODO: 
# - Add depth limit on graph
# - Find way of diplaying graph or better saving mechanism
# - Make larger values of each level more obvious
# - Comments

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
            updateSizes(tree, fullPath, fileSize)
            
    setLabels(tree)    
    tree.save2file("graph.txt")

def initArgParser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="Disk Usage Analyser", description="Plots disk usage in a tree plot")
    parser.add_argument("root", help="The path to the root directory whose contents should be analysed")
    parser.add_argument("-d", "--depth", type=int, help="How deep should the tree be displayed")
    return parser.parse_args()
    
def addFolderNode(tree: Tree, path: Path, node: FolderNode) -> None:
    tree.create_node(node.name,str(path),data=node, parent=str(path.parent))
    
def updateSizes(tree: Tree, path: Path, size:int) -> None:
    try:
        node = tree.get_node(str(path.parent))
    except Exception as e:
        print("Size update failed")
        print(e)
        return
        
    if(node == None):
        return
    
    node.data.addToSize(size) 
    updateSizes(tree, path.parent, size)
    
def setLabels(tree:Tree) -> None:
    for nodeStr in tree.expand_tree():
        node = tree.get_node(nodeStr)
        node.tag = node.data.getLabel()


if __name__ == "__main__":
    main()