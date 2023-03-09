ARG BASE_IMAGE=jupyterhub/jupyterhub
FROM ${BASE_IMAGE}

#RUN pip install --no-cache-dir --upgrade jupyter jupyterlab 
RUN pip install --no-cache-dir jupyter jupyterlab 
RUN pip install --no-cache-dir --upgrade ipython
RUN pip install --no-cache-dir --upgrade dockerspawner
RUN pip install --no-cache-dir jupyterhub-idle-culler
# RUN pip install --no-cache-dir --upgrade oauthenticator
RUN pip install --no-cache-dir --upgrade  jupyterhub-nativeauthenticator
RUN pip install --no-cache-dir --upgrade jupyterhub-ldapauthenticator
RUN pip install --no-cache-dir --upgrade jupyterhub-ltiauthenticator

# COPY jupyterhub_config.py .
# COPY userlist .

EXPOSE 8000

# It seems it is the command to get the verbose output
# https://github.com/jupyterhub/jupyterhub/issues/3671
# CMD jupyterhub -f /srv/jupyterhub/jupyterhub_config.py --debug