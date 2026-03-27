#!/bin/bash
# Stop the FoamAgent container

CONTAINER_NAME="${CONTAINER_NAME:-foamagent}"

if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
    echo "Stopping $CONTAINER_NAME..."
    docker stop $CONTAINER_NAME
    echo "✓ Container stopped"
else
    echo "Container $CONTAINER_NAME is not running"
fi
