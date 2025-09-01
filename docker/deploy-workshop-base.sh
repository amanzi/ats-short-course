#!/bin/bash

# Super basic for now, just to make this easier to share.


# MPI installed in the Docker image
# Options: openmpi, mpich

# Print out options and help statements
Help()
{
    echo "Usage: $(basename $0) [-h|--help] [additional options]"
    echo "Options:"
    echo "  -h, --help          Display this help message"
    echo "  --no_cache          Ignore docker layers in Docker build cache and build from scratch"
    echo "  --output_style      Should we use the condensed or plain version of Docker output (Default: condensed)."
    echo "                      Set --output_style='plain' for expanded output"
    echo "  --multiarch         Build for both linux/amd64 and linux/arm64 instead of only local system architecture"
    echo "                      Assumes your already have Docker configured to build multiarchitecture images"
    echo "  --build_mpi         Should we build the mpi?"
    echo "  --push              Push resulting image to Dockerhub (Requires caution!!)"
    exit 0
}

# parse command line options, if given
for i in "$@"
do
case $i in
    -h|--help)
    Help
    ;;
    --output_style=*)
    output_style="${i#*=}"
    shift
    ;;
    --multiarch)
    multiarch=True
    shift
    ;;
    --build_mpi)
    build_mpi=True
    shift
    ;;
    --push)
    push=True
    shift
    ;;
    --no_cache)
    cache="--no-cache"
    shift
    ;;
    *)
        # unknown option?
    ;;
esac
done

# set defaults, if not given on CLI
output_style="${output_style:-}"
multiarch="${multiarch:-False}"
push="${push:-False}"
build_mpi="${build_mpi:-False}"
cache="${cache:-}"

if [ "${output_style}" = "plain" ]; then
    output="--progress=plain"
else
    output=""
fi

if "${push}" ; then
    push_arg="--push"
else
    if $multiarch ; then
        push_arg="--load"
    else
        push_arg=""
    fi
fi

if $multiarch
then
   docker buildx build \
        --platform=linux/amd64,linux/arm64 \
        ${cache} \
        ${output} \
        ${push_arg} \
        --build-arg build_mpi=${build_mpi} \
        -f ./Dockerfile-Workshop-Base \
        -t metsi/ats-short-course:2025-base .
else
       # --no-cache
   docker build \
       ${cache} \
       ${output} \
       --build-arg build_mpi=${build_mpi} \
       -f ./Dockerfile-Workshop-Base \
       -t metsi/ats-short-course:2025-base .
fi

docker tag metsi/ats-short-course:2025-base metsi/ats-short-course:2025-base