# ATS Shortcourse

[![Docker](https://github.com/amanzi/ats-short-course/actions/workflows/docker-test.yml/badge.svg?branch=main)](https://github.com/amanzi/ats-short-course/actions/workflows/docker-test.yml)

To follow along with the demonstrations, you will perform simulations and visualization results within Jupyter notebooks running under JupyterLab within a Docker container.  The container contains:

* A Linux-based operating system, including common command line tools.
* A build of Amanzi-ATS, with corresponding commonly-used environment variables, e.g. `$ATS_SRC_DIR` defined.
* All needed Third-Party Libraries and utilities (`h5dump`, `ncdump`, `meshconvert`, etc)
* A python3 build with all needed libraries for common ATS-based tasks.
* Watershed Workflow and Tinerator, two common ATS meshing workflow tools.

# Participant: set up for a short course

This has been tested on Linux, Mac OSX, and, to a lesser extent, Windows systems.  The expectation is that this short course should work on any of these systems, but it is our first short course, so please be patient.  If you find bugs in the docker container or this material, please feel free to ask for help on the [ATS user's group](mailto:ats-users@googlegroups.com) or by submitting an Issue here.

## Required Software
As a first step you need to have the following tools installed on your system

* Docker: [Download](https://www.docker.com/get-started)
* VisIt: [Download](https://wci.llnl.gov/simulation/computer-codes/visit/executables)
  * (or ParaView: [Download](https://www.paraview.org/download/) if you prefer it and already know how to use it)
* git (so you can clone this repo):
  * Mac OSX: git is included in the _command line tools_, installed via `xcode-select --install`, or in XCode itself.
  * Linux: git is included as a standard package under most package managers, e.g. `sudo apt-get install git`
  * Windows: see [Git Downloads](https://github.com/git-guides/install-git)

## Getting the Short-course Files

The jupyter notebooks, as well as the corresponding input files and data, are provided in this git repository. To get started you need to clone this repository:

```sh
#
# Select a local directory (here we assume starting at the top-level of your home directory)
#
cd ~/
git clone https://github.com/amanzi/ats-short-course
```

After cloning, change to the repository directory:

``` sh
cd ats-short-course
```

## Download and run ATS in Docker

The Docker container for this short-course includes installations of Watershed Workflow, TINerator, amanzi, and ats.  As a result it is fairly large and best to separate the initial download and testing before we run JupyterLab.  To get started lets download the container:


``` sh
docker pull metsi/ats-short-course:latest
```

If this downloads successful, let's check the version of ATS:

``` sh
docker run -it --rm metsi/ats-short-course:latest ats --version
> ATS version 1.2.0_db31397f
```

If this worked - great!  Move on to "Run JupyterLab under Docker".  But if you ran into trouble with the download and/or docker storage on your system check your configuration with 

``` sh
docker system df
```

And compare the usage ("SIZE") with what you have allocated for space in your Docker "Preferences".  You may see significant space is "RECLAIMABLE".  As a start consider pruning the image layers that aren't connected to images that are being used:

``` sh
docker system prune -f 
```

If you need more space, consider purging all unused images with "-a".

Note also that OSX machines can blank the screen or sleep, both of which can pause the download and not recover.  Setting the battery settings to never blank the screen (preferably when plugged in) and potentially running the ``caffeinate`` command to stop OSX from sleeping may be helpful on slow internet connections.

## Run JupyterLab under Docker

The goal is for you to enable JupyterLab to interact with the ats-short-course repository files on your local system.  This is accomplished through the `-v` or `--volume` option which shares your _present working directory_ (`$pwd`) with the Docker container.  So make sure your `$pwd` is the top-level of the `ats-short-course` repository and cut-and-paste one of the following commands:

```sh
docker run -it -v $(pwd):/home/ats_sc_user/short-course:delegated -w /home/ats_sc_user/short-course -p 8888:8888 metsi/ats-short-course:latest
```

OR if you prefer the verbose version

```sh
docker run \
    --interactive \
    --tty \
    --volume $(pwd):/home/ats_sc_user/short-course:delegated \
    --publish 8888:8888 \
    --workdir /home/ats_sc_user/short-course \
    metsi/ats-short-course:latest
```

This will output several status messages to the screen, one of which is about the Jupyter server that it started.  For example, you should see something like 

``` sh
[I 2021-08-17 21:59:38.111 ServerApp] Jupyter Server 1.10.2 is running at:
# This address is unique to each system, so don't copy this one in your case
[I 2021-08-17 21:59:38.111 ServerApp] http://58557662c177:8888/lab
# This address is generic and will work on any system where this port on local host has not been allocated to another process
[I 2021-08-17 21:59:38.111 ServerApp]  or http://127.0.0.1:8888/lab
# To kill this server
[I 2021-08-17 21:59:38.111 ServerApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
```

Once this is running you can open this URL: (http://127.0.0.1:8888/lab) in your browser and you're ready to go - you should see JupyterLab and the files from this repository.

# Developers

In addition to the notes for Participants, developers may want to additional background information.

## Building Docker Images

If you are interested in building the Docker image, follow these steps:

```sh
#
# Assuming your PWD is the top-level of the repository
#
cd docker/
make all

# Or...
docker build -t metsi/ats-short-course:wwtin-latest -f Dockerfile-Ubuntu-WW+TIN ./
docker build -t metsi/ats-short-course:TPLs-latest -f Dockerfile-Workshop-TPLs ./
docker build -t metsi/ats-short-course:Amanzi-latest -f Dockerfile-Workshop-Amanzi ./
docker build -t metsi/ats-short-course:latest -f Dockerfile-Workshop-ATS ./

```
