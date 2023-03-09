#!/bin/sh

DOCKER_VOLUMES_FOLDER="/var/lib/docker/volumes/"
JUPYTERHUB_VOLUMES=${DOCKER_VOLUMES_FOLDER}/jupyterhub-user-*
JUPYTERHUB_FILE_MAXSIZE=10M

echo "Used disk statistics"
du -hcs $JUPYTERHUB_VOLUMES

echo -e "\nRemoving big files"
find $JUPYTERHUB_VOLUMES -type f -mmin +60 -name "core*" -exec rm {} +
find $JUPYTERHUB_VOLUMES -type f -size +$JUPYTERHUB_FILE_MAXSIZE -exec rm {} +
