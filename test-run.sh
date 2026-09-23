#!/bin/bash
# Test script to run the TVM code with the default configuration.

rm -rf test-run/
mkdir test-run/
cd test-run/
python ../scripts/conf.py
docker build  --platform linux/amd64 -f scripts/tvm/Dockerfile -t tvm-initialization scripts/tvm
docker run --platform linux/amd64 -v $(pwd):/data tvm-initialization
../build/tvm

