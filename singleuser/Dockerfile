ARG JUPYTERHUB_VERSION=3.0.0
FROM jupyter/minimal-notebook:hub-$JUPYTERHUB_VERSION

USER root

# Update current packages and install new ones
RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends \
    net-tools iputils-ping \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Setup default prompt
RUN echo 'export PS1=`echo $JUPYTERHUB_USER| sed s/-at-.*//`"@jupyterhub:\w\$ "' > /etc/profile.d/01-jupyterhub-prompt.sh
# Hack to override the setting of PS1 in the users's bashrc
RUN ln -s /etc/profile.d/01-jupyterhub-prompt.sh /etc/bash_completion
# Switch back to jovyan to avoid accidental container runs as root
USER ${NB_UID}

# TODO: Search why jupyterhub has to be installed
# https://jupyterhub-dockerspawner.readthedocs.io/en/latest/docker-image.html
# https://github.com/jupyter/docker-stacks/blob/main/docs/using/recipes.md
ARG JUPYTERHUB_VERSION=3.0.0
RUN pip install --quiet --no-cache-dir jupyterhub==${JUPYTERHUB_VERSION} && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# A Jupyter kernel for bash
RUN pip install bash_kernel && \
    python -m bash_kernel.install

# Jupytext 
RUN pip install jupytext --upgrade
# RUN jupyter nbextension install --py jupytext --user

# TODO: Use FROM image in order to simplify the Dockerfile
RUN mkdir -p /home/${NB_USER}/shared

ARG BUILD_NOTEBOOK_ARGS="--log-level='DEBUG'"
ENV NOTEBOOK_ARGS=$BUILD_NOTEBOOK_ARGS
