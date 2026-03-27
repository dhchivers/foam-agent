#!/bin/bash
# Build script for FoamAgent Docker container

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "Building FoamAgent Docker container..."
echo "Project directory: $PROJECT_DIR"

# Build the Docker image
docker build -t foamagent:latest \
    -f "$PROJECT_DIR/Dockerfile" \
    "$PROJECT_DIR"

echo ""
echo "✓ Build complete!"
echo ""
echo "To run the container, use: ./scripts/run.sh"
