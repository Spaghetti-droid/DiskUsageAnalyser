from pathlib import Path
import argparse
import humanize
from treelib import Tree, exceptions
from FolderNode import *

# TODO: 
# - Find way of diplaying graph or better saving mechanism
# - Make larger values of each level more obvious
# - Comments

DEFAULT_MIN_SIZE = 100000000
DEFAULT_FILE_LOCATION = "output.txt"

def main():
    args = initArgParser()
    if Path(args.outputFile).exists():
        raise ValueError("Can't output graph: File already exists at '" + args.outputFile + "'")
    maxDepth = args.depth
    initialRoot = Path(args.root)
    tree = Tree()
    rootNode = FolderNode(initialRoot.name)
    tree.create_node(rootNode.name,str(initialRoot),data=rootNode)
    for root, dirs, files in initialRoot.walk(on_error=print):
        try:
            for dir in dirs: 
                addFolderNode(tree, root / dir, FolderNode(dir), maxDepth)
            
            for file in files:
                fullPath = root / file
                fileSize = fullPath.stat().st_size
                updateSizes(tree, fullPath, fileSize)
        except Exception as e:
            print("Error during node addition")
            print(e)
        
            
    setLabels(tree)    
    removeUnwantedNodes(tree, maxDepth, args.minSize)        
    tree.save2file(args.outputFile)

def initArgParser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="analyser.py", description="Plots disk usage in a tree plot")
    parser.add_argument("root", help="The path to the root directory whose contents should be analysed")
    parser.add_argument("-d", "--depth", type=int, help="How many levels of the tree should be displayed. Note that this ONLY affects the display. The analyser will still explore the entire folder hierarchy. Default: no limit.")
    parser.add_argument("-m", "--minSize", type=int, help="The minimum size that an element should have before it is displayed. Any child of a hidden element is also hidden. Default: " + humanize.naturalsize(DEFAULT_MIN_SIZE), default=DEFAULT_MIN_SIZE)
    parser.add_argument("-o", "--outputFile", help="Where to save the result. Default: " + str(DEFAULT_FILE_LOCATION), default=DEFAULT_FILE_LOCATION)

    return parser.parse_args()
    
def addFolderNode(tree: Tree, path: Path, node: FolderNode, maxDepth:int|None) -> None:
    nId = str(path)
    tree.create_node(node.name,nId,data=node, parent=str(path.parent))
    # Only need to remove nodes at max depth. Those below will go with them
    node.toRemove = maxDepth != None and tree.level(nId) == maxDepth+1
    
    
def updateSizes(tree: Tree, path: Path, size:int) -> None:
    try:
        node = tree.get_node(str(path.parent))
        while node != None:
            node.data.addToSize(size) 
            node = tree.parent(node.identifier)
    except Exception as e:
        print("Size update failed")
        print(e)
    
def setLabels(tree:Tree) -> None:
    for nodeStr in tree.expand_tree():
        node = tree.get_node(nodeStr)
        node.tag = node.data.getLabel()

def removeUnwantedNodes(tree:Tree, maxDepth:int|None, releventSize:int) -> None:
    if(maxDepth != None or releventSize > 0):
        # Do this in 2 goes to avoid upsetting the tree
        nodes = []
        for node in tree.filter_nodes(lambda x:x.data.toRemove or (x.data.size < releventSize)):
            nodes.append(node)
        
        for node in nodes:
            try:
                tree.remove_node(node.identifier)
            except exceptions.NodeIDAbsentError:
                # Not really a problem
                pass

if __name__ == "__main__":
    main()