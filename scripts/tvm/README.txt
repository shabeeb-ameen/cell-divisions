Scripts:
1. sample.py: 
    action: from a Voronoi tessellation of 20*20*20 cells, select a spheroid of radius 4.0 (the rest are "empty cells")
    - output: creates sample.txt
2. ECM64.py:
    action: creates fcc lattice, fills edges with probability p (first line, main function)
    - output: creates ECM.txt

Note: These scripts (or at least, "sample2_5.py") needs a specific version of pyvoro.
See more about pyvoro in https://github.com/joe-jordan/pyvoro.

Networkx is used in ECM64.py.

Recommended usage: use the Docker container, which runs both these scripts.