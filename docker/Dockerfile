# hacked together from WW, Amanzi-TPL, and ATS dockerfiles

#
# Stage 1 -- setup compilers, apt-get environment, and conda environments
#
FROM condaforge/miniforge3:latest AS base_ubuntu_conda
LABEL Description="ATS 2025 Short Course Container"

ENV CONDA_BIN=mamba
ARG env_name=watershed_workflow
ARG build_mpi=True
ARG mpi_flavor=mpich
ARG mpi_version=4.0.3

# install system tools:
RUN apt-get -q update -y && apt-get install -y tzdata && \
  apt-get -q install -y \
  apt-utils \
  curl \
  libcurl4-openssl-dev \
  emacs \
  gedit \
  git \
  g++ \
  gfortran \
  gcc \ 
  groff \
  libblas-dev \
  liblapacke-dev \
  liblapack-dev \
  libssl-dev \
  m4 \
  # bootstrap will get cmake
  make \ 
  openssl \
  pkg-config \
  rsync \
  wget \
  vim \
  zlib1g-dev && \
  apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# install MPI - if mpich, custom compile; if openmpi, install precompiled binary
RUN if [ "$build_mpi" = "True" ]; then \
  if [ "$mpi_flavor" = "mpich" ]; then cd / \
  && wget https://www.mpich.org/static/downloads/${mpi_version}/mpich-${mpi_version}.tar.gz \
  && tar xvf mpich-${mpi_version}.tar.gz \
  && cd mpich-${mpi_version} \
  && FFLAGS="-fallow-argument-mismatch" FCFLAGS="-fallow-argument-mismatch" ./configure --enable-shared --with-device=ch3:sock --enable-fast=all,Os --prefix=/usr/local \
  && make -j4 \
  && make install \
  && cd ../ \
  && rm -r mpich-${mpi_version}/ \
  && rm mpich-${mpi_version}.tar.gz ; \
  elif [ "$mpi_flavor" = "openmpi" ]; then cd / \
  && export mpi_version_major=`echo ${mpi_version} | cut -c1-3` && echo $mpi_version_major \
  && wget https://download.open-mpi.org/release/open-mpi/v${mpi_version_major}/openmpi-${mpi_version}.tar.gz \
  && tar xvf openmpi-${mpi_version}.tar.gz \
  && cd openmpi-${mpi_version} \
  && export LD_LIBRARY_PATH=/usr/local/lib64:/usr/local/lib:$LD_LIBRARY_PATH \
  && FFLAGS="-fallow-argument-mismatch" FCFLAGS="-fallow-argument-mismatch" ./configure --enable-shared --prefix=/usr/local \
  && make -j4 \
  && make install \
  && cd ../ \
  && rm -r openmpi-${mpi_version}/ \
  && rm openmpi-${mpi_version}.tar.gz ; \
  else \
  echo "Unknown mpi_flavor - exiting." \
  && exit 1 ; \
  fi \
  else apt-get install -y lib${mpi_flavor}-dev ; fi


# change to release branch later (or wget tar for release)
RUN git clone -b master --depth=1 https://github.com/environmental-modeling-workflows/watershed-workflow /ww \
  && mkdir /ww/tmp \
  && cp /ww/environments/create_envs.py /ww/tmp/create_envs.py \
  && cd /ww/tmp \
  && mkdir environments && \
    /opt/conda/bin/python create_envs.py --OS=Linux --manager=${CONDA_BIN}  \
    --env-type=STANDARD --with-user-env=${env_name}-USER ${env_name}

WORKDIR /ww/tmp
RUN cp /ww/requirements.txt /ww/tmp/ && ${CONDA_BIN} run --name ${env_name} python -m pip install -r requirements.txt

#
# Stage 3 -- build amanzi tpls
# 

FROM base_ubuntu_conda AS tpls

WORKDIR /amanzi/tmp
RUN git clone --depth=1 https://github.com/amanzi/amanzi \ 
  && cd amanzi \
  && ./bootstrap.sh --prefix=${AMANZI_PREFIX} \
  --parallel=4 --opt \
  --amanzi-build-dir=/amanzi/tmp/amanzi_builddir/amanzi \
  --tpl-build-dir=/amanzi/tmp/amanzi_builddir/tpls \
  --tpl-download-dir=/amanzi/tmp/amanzi_builddir/tpls/Downloads \
  --disable-build_amanzi --disable-build_user_guide \
  --enable-shared --enable-structured --enable-silo \
  --enable-alquimia --enable-pflotran --enable-crunchtope \
  --enable-pf_clm \
  --with-mpi=/usr/local \
  --with-python=/opt/conda/bin/python


#
# Stage 4 - build ATS
#

WORKDIR /amanzi/tmp
RUN cd amanzi && git submodule update --init --recursive \
  && ./bootstrap.sh --prefix=${AMANZI_PREFIX} \
   --amanzi-build-dir=/home/amanzi_user/amanzi_builddir/ats \
   --tpl-config-file=${AMANZI_TPLS_DIR}/share/cmake/amanzi-tpl-config.cmake \
   --parallel=4 \
   --opt \
   --with-mpi=/usr \
   --enable-shared \
   --disable-structured \
   --disable-build_user_guide \
   --enable-geochemistry \
   --disable-amanzi_physics \
   --enable-ats_physics \
   --ats_dev \
   --enable-reg_tests \
   --enable-test_suite
