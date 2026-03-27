#!/bin/bash
# Run script for FoamAgent Docker container

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Create work directory if it doesn't exist
WORK_DIR="$PROJECT_DIR/work"
mkdir -p "$WORK_DIR"

# Configuration
VNC_PASSWORD="${VNC_PASSWORD:-foamagent}"
VNC_RESOLUTION="${VNC_RESOLUTION:-1920x1080}"
CONTAINER_NAME="${CONTAINER_NAME:-foamagent}"

# Stop and remove existing container if it exists
if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    echo "Stopping existing container..."
    docker stop $CONTAINER_NAME 2>/dev/null || true
    docker rm $CONTAINER_NAME 2>/dev/null || true
fi

echo "Starting FoamAgent container..."
echo "VNC Resolution: $VNC_RESOLUTION"
echo "Work directory: $WORK_DIR"

# Run the container
docker run -d \
    --name $CONTAINER_NAME \
    -p 5901:5901 \
    -p 6080:6080 \
    -v "$WORK_DIR:/work" \
    -e VNC_RESOLUTION="$VNC_RESOLUTION" \
    -e VNC_PASSWORD="$VNC_PASSWORD" \
    --shm-size=2g \
    foamagent:latest

# Wait for services to start
echo "Waiting for services to start..."
sleep 5

echo ""
echo "✓ FoamAgent is running!"
echo ""
echo "Access the GUI via web browser:"
echo "  http://localhost:6080"
echo ""
echo "VNC direct access:"
echo "  vnc://localhost:5901"
echo ""
echo "To view logs:"
echo "  docker logs -f $CONTAINER_NAME"
echo ""
echo "To stop:"
echo "  docker stop $CONTAINER_NAME"
echo ""
