# hacked together from WW, Amanzi-TPL, and ATS dockerfiles

#
# Stage 1 -- setup tpls
#

FROM ubuntu:jammy AS base_ubuntu
LABEL Description="ATS 2025 Short Course Container"

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
  libmpich-dev \
  libssl-dev \
  m4 \
  make \
  openssl \
  pkg-config \
  rsync \
  wget \
  vim \
  zlib1g-dev && \
  apt-get clean \
  && rm -rf /var/lib/apt/lists/*


# Add an unprivileged user and group: amanzi_user, amanzi_user
RUN groupadd -r amanzi_user \
  && useradd -r -K UMASK=0022 -K HOME_MODE=0755 -m -g amanzi_user amanzi_user 

#
# Stage 2 - install miniforge
#

FROM base_ubuntu AS conda
ENV CONDA_DIR=/opt/conda
ARG MINIFORGE_NAME=Miniforge3
ARG MINIFORGE_VERSION=25.3.0-3
RUN wget --no-hsts --quiet https://github.com/conda-forge/miniforge/releases/download/${MINIFORGE_VERSION}/${MINIFORGE_NAME}-${MINIFORGE_VERSION}-Linux-$(uname -m).sh -O /tmp/miniforge.sh && \
    /bin/bash /tmp/miniforge.sh -f -b -p ${CONDA_DIR} && \
    rm /tmp/miniforge.sh && \
    echo ". ${CONDA_DIR}/etc/profile.d/conda.sh && conda activate base" >> /etc/skel/.bashrc && \
    echo ". ${CONDA_DIR}/etc/profile.d/conda.sh && conda activate base" >> ~/.bashrc 

# Set PATH for future RUN commands
ENV PATH="${CONDA_DIR}/bin:$PATH"


ENV CONDA_BIN=mamba
ARG env_name=watershed_workflow


FROM conda AS ww


# change to release branch later (or wget tar for release)
RUN git clone -b master --depth=1 https://github.com/environmental-modeling-workflows/watershed-workflow /ww \
  && cd /ww \
  && /opt/conda/bin/python environments/create_envs.py --OS=Linux --manager=${CONDA_BIN}  \
    --env-type=STANDARD --with-user-env=${env_name}-USER ${env_name}

WORKDIR /ww
RUN ${CONDA_BIN} run --name ${env_name} python -m pip install -r requirements.txt \
    && ${CONDA_BIN} install numpy

#
# Stage 2 -- build amanzi tpls
# 

FROM ww AS tpls

# Versions change and we cannot set environment variables from command output.
ARG petsc_ver=3.20
ARG trilinos_ver=15-1-0
ARG amanzi_branch=amanzi-1.6

# Installation paths
ENV AMANZI_PREFIX=/home/amanzi_user/install \
  AMANZI_INSTALL_DIR=/home/amanzi_user/install/amanzi \
  AMANZI_TPLS_DIR=/home/amanzi_user/install/tpls

# TPL versions needed for LD_LIBRARY_PATH
ENV AMANZI_PETSC_LIBS=$AMANZI_TPLS_DIR/petsc-${petsc_ver}/lib \
  AMANZI_TRILINOS_LIBS=$AMANZI_TPLS_DIR/trilinos-${trilinos_ver}/lib \
  AMANZI_SEACAS_LIBS=$AMANZI_TPLS_DIR/SEACAS/lib


# Set the current working directory as the users home directory
# (creates the directory if it doesn't exist)
WORKDIR /home/amanzi_user

RUN git clone -b amanzi-1.6 --depth=1 https://github.com/amanzi/amanzi \ 
  && cd amanzi \
  # && ./bootstrap.sh --prefix=${AMANZI_PREFIX} \
  # --parallel=4 --opt \
  # --amanzi-build-dir=/home/amanzi_user/amanzi_builddir/amanzi \
  # --tpl-build-dir=/home/amanzi_user/amanzi_builddir/tpls \
  # --tpl-download-dir=/home/amanzi_user/amanzi_builddir/tpls/Downloads \
  # --disable-build_amanzi --disable-build_user_guide \
  # --enable-shared --disable-structured --disable-silo \
  # --enable-alquimia --enable-pflotran --enable-crunchtope \
  # --disable-pf_clm \
  # --with-mpi=/usr \
  # --with-python=$(which python)

#
# Stage 3 - build ATS
#

FROM tpls AS ats_build

WORKDIR /home/amanzi_user
RUN cd amanzi && git submodule update --init --recursive \
  # && ./bootstrap.sh --prefix=${AMANZI_PREFIX} \
  #  --amanzi-build-dir=/home/amanzi_user/amanzi_builddir/ats \
  #  --tpl-config-file=${AMANZI_TPLS_DIR}/share/cmake/amanzi-tpl-config.cmake \
  #  --parallel=4 \
  #  --opt \
  #  --with-mpi=/usr \
  #  --enable-shared \
  #  --disable-structured \
  #  --disable-build_user_guide \
  #  --enable-geochemistry \
  #  --disable-amanzi_physics \
  #  --enable-ats_physics \
  #  --ats_dev \
  #  --enable-reg_tests \
  #  --enable-test_suite


# FROM ats_build AS test

# WORKDIR /home/amanzi_user/amanzi_builddir/ats
# RUN ctest --output-on-failure

# WORKDIR /ww
# RUN pytest