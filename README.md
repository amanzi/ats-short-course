# ATS Shortcourse

[![Docker](https://github.com/amanzi/ats-short-course/actions/workflows/docker-test.yml/badge.svg?branch=main)](https://github.com/amanzi/ats-short-course/actions/workflows/docker-test.yml)

Files related to the Amanzi Workshop.

## Prerequisites for the Short Course
* Docker
* VisIt (or ParaView if you prefer and know what you are doing)
* git (so you can clone this repo)

## Docker

To build,

```sh
$ cd docker/
$ make all

# Or...
$ docker build -t metsi/workshop21:wwtin-latest -f Dockerfile-Ubuntu-WW+TIN ./
$ docker build -t metsi/workshop21:TPLs-latest -f Dockerfile-Workshop-TPLs ./
$ docker build -t metsi/workshop21:Amanzi-latest -f Dockerfile-Workshop-Amanzi ./
$ docker build -t metsi/workshop21:latest -f Dockerfile-Workshop-ATS ./

# Or...
$ docker pull metsi/workshop21:latest
```

To run,

```sh
$ docker run -it -v $(pwd):/home/amanzi_user/work  -w /home/amanzi_user/work -p 8888:8888 metsi/workshop21:latest

$ docker run \
    --interactive \
    --tty \
    --volume $(pwd):/home/amanzi_user/work \
    --publish 8888:8888 \
    --workdir /home/amanzi_user/work \
    metsi/workshop21:latest
```
