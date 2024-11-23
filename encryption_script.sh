#!/bin/bash

set -e

ENCRYPTION_SERVICE_IMAGE="akshat315/encryption-service:latest"

ENCRYPTION_CONTAINER="encryption-service"

ENCRYPTION_PORT=8001

DOCKER_NETWORK="app-network"

# Check if Docker network exists, if not, create it
if [ -z "$(docker network ls --filter name=^${DOCKER_NETWORK}$ --format="{{ .Name }}")" ]; then
    echo "Creating Docker network: ${DOCKER_NETWORK}"
    docker network create ${DOCKER_NETWORK}
fi

echo "Stopping existing containers if any..."

docker stop -f ${ENCRYPTION_CONTAINER} > /dev/null 2>&1 || true

echo "Starting Encryption Service..."
docker run -d \
    --name ${ENCRYPTION_CONTAINER} \
    --network ${DOCKER_NETWORK} \
    -p ${ENCRYPTION_PORT}:8001 \
    ${ENCRYPTION_SERVICE_IMAGE}

echo "Container is up and running."

docker ps --filter "name=${CONVERTER_CONTAINER}" --filter "name=${ENCRYPTION_CONTAINER}"
