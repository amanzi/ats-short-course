# ATS Shortcourse

[![Docker](https://github.com/amanzi/ats-short-course/actions/workflows/docker-test.yml/badge.svg)](https://github.com/ats-short-course/workshop/actions/workflows/docker-test.yml)
`
Files related to the Amanzi Workshop.

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
```
