# hacked together from WW, Amanzi-TPL, and ATS dockerfiles

#
# Stage 1 -- setup base CI environment
#
FROM condaforge/miniforge3:latest AS ww_env_base_ci
LABEL Description="Base env for CI of Watershed Workflow"

ARG env_name=watershed_workflow_CI
ENV CONDA_BIN=mamba

WORKDIR /ww/tmp
# COPY environments/create_envs.py /ww/tmp/create_envs.py 
# RUN mkdir environments

# install a base environment with just python
RUN ${CONDA_BIN} install -n base -y -c conda-forge python=3.13 gcc g++ gfortran mpich

#RUN --mount=type=cache,target=/opt/conda/pkgs \
#    /opt/conda/bin/python create_envs.py --OS=Linux --manager=${CONDA_BIN}  \
#    --env-type=CI --with-tools-env=watershed_workflow_tools ${env_name}

ENV COMPILERS=/opt/conda/envs/base 
ENV PATH="$COMPILERS/bin:$PATH"
ENV CC=$COMPILERS/bin/gcc
ENV CXX=$COMPILERS/bin/g++
ENV FC=$COMPILERS/bin/gfortran
ENV AR=$COMPILERS/bin/gcc-ar
ENV RANLIB=$COMPILERS/bin/gcc-ranlib

#
# Stage 2 -- add in the pip
#
FROM ww_env_base_ci AS ww_env_pip_ci

# WORKDIR /ww/tmp
# COPY requirements.txt /ww/tmp/requirements.txt
# RUN ${CONDA_BIN} run --name ${env_name} python -m pip install -r requirements.txt

#
# Stage 3 -- build amanzi tpls
# 
WORKDIR /amanzi/tmp
RUN git clone --depth=1 git@github.com:amanzi/amanzi \ 
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
  --with-mpi=/opt/conda/envs/base/ \
  --with-python=/opt/conda/envs/base