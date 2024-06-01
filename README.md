# Disk Usage Analyser

For any given folder, creates a tree of its descendants, showing how much space is taken by each. This tree is saved in a file called 'output.txt' by default.

## Example

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
