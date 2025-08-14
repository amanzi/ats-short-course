#!/bin/bash

# Super basic for now, just to make this easier to share.

# Could add some build args here.


docker build \
       --no-cache \
       --progress=plain \
       -f ./Dockerfile-Workshop-ATS -t metsi/ats-short-course:2025-ats .




