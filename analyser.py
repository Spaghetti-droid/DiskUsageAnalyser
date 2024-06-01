import argparse
import humanize
from pathlib import Path
from treelib import Tree, exceptions
from FolderNode import *

# TODO: 
# - Find way of diplaying graph
# - Make larger values of each level more obvious

DEFAULT_MIN_SIZE = 100_000_000
DEFAULT_FILE_LOCATION = "output.txt"

def main():
    
    # Get arguments from user
    
    args = initArgParser()
    if Path(args.outputFile).exists():
        raise ValueError("Can't output graph: File already exists at '" + args.outputFile + "'")
    maxDepth = args.depth
    initialRoot = Path(args.root)
    
    # Initialise tree and set root node
    
    tree = Tree()
    rootNode = FolderNode(initialRoot.name)
    tree.create_node(rootNode.name,str(initialRoot),data=rootNode)
    
    # Go though folder hierarchy
    
    for root, dirs, files in initialRoot.walk(on_error=print):
        try:
            for dir in dirs: 
                # Add to tree
                addFolderNode(tree, root / dir, FolderNode(dir), maxDepth)
            
            for file in files:
                # Update ancestor's size but do not add to tree to avoid clutter
                fullPath = root / file
                fileSize = fullPath.stat().st_size
                updateSizes(tree, fullPath, fileSize)
        except Exception as e:
            print("Error during node addition")
            print(e)
        
    # Format tree into it's displayed form
            
    setLabels(tree)    
    removeUnwantedNodes(tree, maxDepth, args.minSize)
    
    # Save
            
    tree.save2file(args.outputFile)

def initArgParser() -> argparse.Namespace:
    """Defines the arguments that the program can use

    Returns:
        argparse.Namespace: The argument values the user specified to the application
    """
    parser = argparse.ArgumentParser(prog="analyser.py", description="Plots disk usage in a tree plot")
    parser.add_argument("root", help="The path to the root directory whose contents should be analysed")
    parser.add_argument("-d", "--depth", type=int, help="How many levels of the tree should be displayed. Note that this ONLY affects the display. The analyser will still explore the entire folder hierarchy. Default: no limit.")
    parser.add_argument("-m", "--minSize", type=int, help="The minimum size in bytes that an element should have before it is displayed. Any child of a hidden element is also hidden. Default: " + str(DEFAULT_MIN_SIZE) + " (" + humanize.naturalsize(DEFAULT_MIN_SIZE) + ")" , default=DEFAULT_MIN_SIZE)
    parser.add_argument("-o", "--outputFile", help="Where to save the result. Default: " + str(DEFAULT_FILE_LOCATION), default=DEFAULT_FILE_LOCATION)

    return parser.parse_args()
    
def addFolderNode(tree: Tree, path: Path, node: FolderNode, maxDepth:int|None) -> None:
    """Add folder node to the tree representing the folder hierarchy

    Args:
        tree (Tree): The tree to update
        path (Path): Path to the folder. The string form of this will be used as the node ID in the tree.
        node (FolderNode): The node to add
        maxDepth (int | None): Determines whether the node will be removed before saving
    """
    nId = str(path)
    tree.create_node(node.name,nId,data=node, parent=str(path.parent))
    # Only need to remove nodes at max depth. Those below will go with them
    node.toRemove = maxDepth != None and tree.level(nId) == maxDepth+1
    
    
def updateSizes(tree: Tree, path: Path, size:int) -> None:
    """Travel through all nodes representing the ancestors of the current path and update their size parameter.
    Essentially, we are adding a file's size to all folders that contain it directly or indirectly.

    Args:
        tree (Tree): Tree to update
        path (Path): Path to the file who's ancestors need updating
        size (int): File size to be added to all ancestors' file sizes
    """
    try:
        node = tree.get_node(str(path.parent))
        while node != None:
            node.data.addToSize(size) 
            node = tree.parent(node.identifier)
    except Exception as e:
        print("Size update failed")
        print(e)
    
def setLabels(tree:Tree) -> None:
    """Visit every node of the tree and set the label to display. 
    The label follows the pattern '<Name> - <size>'

    Args:
        tree (Tree): Tree to update
    """
    for nodeStr in tree.expand_tree():
        node = tree.get_node(nodeStr)
        node.tag = node.data.generateLabel()

def removeUnwantedNodes(tree:Tree, maxDepth:int|None, releventSize:int) -> None:
    """Go through tree and remove all nodes that won't be shown to user

    Args:
        tree (Tree): Tree to update
        maxDepth (int | None): Any node below this depth will be removed
        releventSize (int): Any node below this size will be removed
    """
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