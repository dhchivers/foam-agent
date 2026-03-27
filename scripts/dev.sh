#!/bin/bash
# Development mode script - runs container with live code mounting

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

WORK_DIR="$PROJECT_DIR/work"
mkdir -p "$WORK_DIR"

VNC_RESOLUTION="${VNC_RESOLUTION:-1920x1080}"
CONTAINER_NAME="${CONTAINER_NAME:-foamagent-dev}"

# Stop and remove existing container if it exists
if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    echo "Stopping existing dev container..."
    docker stop $CONTAINER_NAME 2>/dev/null || true
    docker rm $CONTAINER_NAME 2>/dev/null || true
fi

echo "Starting FoamAgent in development mode..."
echo "Source code will be mounted for live editing"

docker run -d \
    --name $CONTAINER_NAME \
    -p 5901:5901 \
    -p 6080:6080 \
    -v "$WORK_DIR:/work" \
    -v "$PROJECT_DIR/src:/app/src" \
    -v "$PROJECT_DIR/ui:/app/ui" \
    -e VNC_RESOLUTION="$VNC_RESOLUTION" \
    --shm-size=2g \
    foamagent:latest

echo ""
echo "✓ Development container running!"
echo ""
echo "To rebuild the application inside the container:"
echo "  docker exec -it $CONTAINER_NAME bash -c 'cd /app/build && cmake .. && make'"
echo ""
echo "Access at: http://localhost:6080"
echo ""
