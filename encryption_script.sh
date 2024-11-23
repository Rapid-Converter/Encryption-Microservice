#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Define Docker image names and versions
ENCRYPTION_SERVICE_IMAGE="akshat315/encryption-service:latest"

# Define container names
ENCRYPTION_CONTAINER="encryption-service"

# Define ports
ENCRYPTION_PORT=8001

# Define Docker network (optional for inter-service communication)
DOCKER_NETWORK="app-network"

# Check if Docker network exists, if not, create it
if [ -z "$(docker network ls --filter name=^${DOCKER_NETWORK}$ --format="{{ .Name }}")" ]; then
    echo "Creating Docker network: ${DOCKER_NETWORK}"
    docker network create ${DOCKER_NETWORK}
fi

# Stop and remove existing containers if they exist
echo "Stopping existing containers if any..."

docker stop -f ${ENCRYPTION_CONTAINER} > /dev/null 2>&1 || true

# Run the Encryption Service container
echo "Starting Encryption Service..."
docker run -d \
    --name ${ENCRYPTION_CONTAINER} \
    --network ${DOCKER_NETWORK} \
    -p ${ENCRYPTION_PORT}:8001 \
    ${ENCRYPTION_SERVICE_IMAGE}

echo "Container is up and running."

# Optional: Display running containers
docker ps --filter "name=${CONVERTER_CONTAINER}" --filter "name=${ENCRYPTION_CONTAINER}"
