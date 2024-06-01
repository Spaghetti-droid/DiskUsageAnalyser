# Disk Usage Analyser

For any given folder, creates a tree of its descendants, showing how much space is taken by each. This tree is saved in a file called 'output.txt' by default.

## Usage

See the help message for details on how to use the program

    analyser.py -h
    usage: analyser.py [-h] [-d DEPTH] [-m MINSIZE] [-o OUTPUTFILE] root

    Plots disk usage in a tree plot

    positional arguments:
      root                  The path to the root directory whose contents should be analysed

    options:
      -h, --help            show this help message and exit
      -d DEPTH, --depth DEPTH
                            How many levels of the tree should be displayed. Note that this ONLY affects the display. The
                            analyser will still explore the entire folder hierarchy. Default: no limit.
      -m MINSIZE, --minSize MINSIZE
                            The minimum size in bytes that an element should have before it is displayed. Any child of a
                            hidden element is also hidden. Default: 100000000 (100.0 MB)
      -o OUTPUTFILE, --outputFile OUTPUTFILE
                            Where to save the result. Default: output.txt

## Requirements and Dependencies

Disk Usage Analyser requires python 3.12 to run.

Disk Usage Analyser depends on several libraries, namely:
- argparse
- humanize
- pathlib
- treelib

Be sure to install any missing ones with

    pip install <library>

## Examples

### Example 1

Running: 

    analyser.py -m 100000 Test
Produces:

    Test - 835.7 MB
    ├── A - 740.2 MB
    │   └── B - 740.2 MB
    │       └── Fish - 740.2 MB
    │           ├── Anchovy - 33.6 MB
    │           ├── Carp - 2.6 MB
    │           ├── Catfish - 4.5 MB
    │           ├── Cod - 974.8 kB
    │           ├── Eel - 17.9 MB
    │           ├── Flounder - 3.8 MB
    │           ├── Goby - 5.2 MB
    │           ├── Koi - 542.9 MB
    │           ├── Loach - 3.8 MB
    │           ├── Marlin - 2.8 MB
    │           ├── Mudskipper - 2.6 MB
    │           ├── Mullet - 1.9 MB
    │           ├── Pike - 34.2 MB
    │           ├── Salmon - 41.9 MB
    │           ├── Shark - 104.0 kB
    │           ├── Sturgeon - 6.9 MB
    │           ├── Sword - 10.5 MB
    │           ├── Tetra - 2.2 MB
    │           └── Trout - 21.9 MB
    └── C - 95.5 MB
        └── Not fish - 95.5 MB
          └── jpg - 38.1 MB

### Example 2

Running:

    analyser.py -d 3 -m 100000 Test

Produces:

    Test - 835.7 MB
    ├── A - 740.2 MB
    │   └── B - 740.2 MB
    │       └── Fish - 740.2 MB
    └── C - 95.5 MB
        └── Not fish - 95.5 MB
            └── jpg - 38.1 MB  


### Example 3

Running:

    analyser.py -d 2 -m 0 Test

Produces:

    Test - 835.7 MB
    ├── A - 740.2 MB
    │   ├── A - 0 Bytes
    │   └── B - 740.2 MB
    ├── B - 0 Bytes
    └── C - 95.5 MB
        └── Not fish - 95.5 MB
