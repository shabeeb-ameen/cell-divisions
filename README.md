# TVM [![Build Status][1]][2] [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

[1]: https://travis-ci.com/ZhangTao-SJTU/tvm.svg?token=YPqm5yHsQT7PD3VM6WG5&branch=main
[2]: https://travis-ci.com/ZhangTao-SJTU/tvm

Embedded 3D vertex model spheroid in fiber network 

Author:

Tao Zhang @ Shanghai Jiao Tong University, zhangtao.scholar@sjtu.edu.cn

Jennifer Schwarz @ Syracuse University, jschwarz@physics.syr.edu

#### Shabeeb's Fork
This fork from Shabeeb Ameen includes python scripts for analyzing results etc. Documentation in progress.

## Description
This code is based on Okuda 2013 paper: https://link.springer.com/article/10.1007/s10237-012-0430-7.

- The network topology satisfies the following conditions:
  1. Two edges never share two vertices simultaneously.
  2. Two polygonal faces never share two or more edges simultaneously.
  3. **EXTRA RULE** Two polyhedral cells never share two or more polygonal faces simultaneously

The scripts are in the folder "scripts" on the main branch.

Current version of the code works ONLY for bulk system with periodic boundary condition. 

Should you receive any warning prompts, please reach out to us as we work towards making the code more robust for more general geometries, deformations, and energy functionals. 

## Quick Start

### TLDR: 
Install CMake and Docker, then from the root directory of this project, then run

    ./compile.sh && ./test-run.sh
    
If the code runs, you are set. The rest of this section describes the bash commands contained in these two scripts.

### Requirements
+ CMake (for compiling the tvm executable)
+ Docker (for running the initialization python scripts)


#### Compiling (C++ codebase and initialization scripts)


+ From root directory of this project, run the following:

        cmake -B build && cmake --build build
        docker build  --platform linux/amd64 -f scripts/tvm/Dockerfile -t tvm-initialization scripts/tvm

(the --platform linux/amd64 is required for apple silicon...)

+ Alternatively: the bashscript compile.sh removes any existing build/ folder and runs the above two commands.

        chmod +x compile.sh && ./compile.sh

#### Usage and program flow:
The following section is meant to be a tutorial for running the code on your machine for the first time (after compiling). All the bash commands below are contained in test-run.sh in the root dir (WARNING: the script first erases any existing "test-run/" folder.)

1. Create a run folder. The rest of this subsection follows after we create and change directory to "test-run/", to be created in the root directory of this project.

    That is, from the root directory of this project:

        mkdir test-run/ && cd test-run/

2. Initialization: Populate the run folder with 
    + conf
    + sample.topo (spheroid topology)
    + ECM.topo (fiber network topology)

    Sample contents of the conf file:

        time 0 2000 0.005
        dump vtk 100.0
        log 10.0
        s0 5.2 1.00
        Lth 0.02
        T 1e-4
        kv 10.
        box 64. 64. 64. p p p
        fiber 10.0 2.8284271 0.001
        link 100 10. 1.5 0.2 0.004 1000.

    You can use the scripts/conf.py to create a conf file with these values. The variable names in this python script document what each parameter is.
        
        python ../scripts/conf.py

    The initial topologies can be created using the docker container:

        docker run --platform linux/amd64 -v $(pwd):/data tvm-initialization





3. Run the `tvm` executable in 'build/'

        ../build/tvm


## License

[GNU GPL v3 License](./LICENSE.md)

Copyright 2021-2023 Tao Zhang
