#!/bin/bash

# This script deletes the build/ folder (if it exists) and compiles the project using CMake
# Output: builds the C++ executable build/tvm

# Requirements:
# CMake version>=3.1

# Usage: 
# To run this script from a terminal:
# 1. Navigate to the project's root folder (where this script should be located...)
# 2. Run the following command in the terminal: chmod +x compile.sh && ./compile.sh

rm -rf build/*
cmake -B build && cmake --build build

# (Single function script. Additionaly you can build the docker machine by uncommenting below...)
# docker build  --platform linux/amd64 -f scripts/tvm/Dockerfile -t tvm-initialization scripts/tvm