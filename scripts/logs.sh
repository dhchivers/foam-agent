#!/bin/bash
# View logs from the FoamAgent container

CONTAINER_NAME="${CONTAINER_NAME:-foamagent}"

if [ ! "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    echo "Container $CONTAINER_NAME does not exist"
    exit 1
fi

echo "Showing logs for $CONTAINER_NAME (Ctrl+C to exit)..."
echo "=================================================="
docker logs -f $CONTAINER_NAME
