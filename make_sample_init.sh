#!/bin/bash
# Creates sample_init/
# This folder contains a sample initial configuration for an embedded spheroid.
# Important: You need to have Docker installed and running to use this script.
docker build  --platform linux/amd64 -f scripts/tvm/Dockerfile -t tvm-initialization scripts/tvm
rm -rf sample_init/
mkdir sample_init/
cd sample_init/
python ../scripts/conf.py
docker run --platform linux/amd64 -v $(pwd):/data tvm-initialization

