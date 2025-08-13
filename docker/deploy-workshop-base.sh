#!/bin/bash

# Super basic for now, just to make this easier to share.


# MPI installed in the Docker image
# Options: openmpi, mpich

build_mpi=FALSE

# --no-cache
docker build \
       --no-cache \
       --progress=plain \
       --build-arg build_mpi=${build_mpi} \
       -f ./Dockerfile-Workshop-Base -t metsi/ats-short-course:2025-base .

