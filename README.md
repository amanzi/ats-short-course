# Amanzi Workshop

[![Docker](https://github.com/amanzi/workshop/actions/workflows/docker-test.yml/badge.svg)](https://github.com/amanzi/workshop/actions/workflows/docker-test.yml)

Files related to the Amanzi Workshop.

## Prerequisites for the Short Course
* Docker
* VisIt (or ParaView if you prefer and know what you are doing)
* git (so you can clone this repo)

## Docker

A Dockerfile is available under `docker/dockerfile`.

To build,

```sh
$ docker build -t amanzi/workshop:latest -f docker/Dockerfile .
```
