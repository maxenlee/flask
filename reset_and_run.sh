#!/bin/bash

# Stop all running containers
docker stop $(docker ps -aq)

# Remove all containers
docker rm $(docker ps -aq)

# Remove all images
docker rmi $(docker images -q)

# Rebuild the Docker image
docker build -t myflask .

# Run the container with pickle_blob.py as the entry point
docker container run \
  --rm \
  --detach \
  --publish 5000:5000 \
  --env PICKLEJAR_ACCESS=${PICKLEJAR_ACCESS} \
  --env PICKLEJAR_SECRET=${PICKLEJAR_SECRET} \
  --name flask \
  myflask python pickle_blob.py
