#!/usr/bin/env bash
# FoamAgent Quick Setup and Launch Script

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                     FoamAgent Setup                            ║"
echo "║    Qt6 OpenFOAM GUI with Web-Based Visualization               ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed"
    echo ""
    echo "Please install Docker:"
    echo "  macOS:   Download from https://www.docker.com/products/docker-desktop"
    echo "  Linux:   sudo apt-get install docker.io"
    echo "  Windows: Download from https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Check Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Error: Docker is not running"
    echo ""
    echo "Please start Docker Desktop or the Docker daemon"
    exit 1
fi

echo "✓ Docker is installed and running"
echo ""

# Check if image exists
if [[ "$(docker images -q foamagent:latest 2> /dev/null)" == "" ]]; then
    echo "📦 Docker image not found. Building..."
    echo "   This will take 10-20 minutes on first run."
    echo ""
    read -p "Continue with build? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
    
    "$SCRIPT_DIR/scripts/build.sh"
    echo ""
else
    echo "✓ Docker image found"
    echo ""
fi

# Check if container is already running
if [ "$(docker ps -q -f name=foamagent)" ]; then
    echo "ℹ️  Container is already running"
    echo ""
else
    echo "🚀 Starting FoamAgent..."
    "$SCRIPT_DIR/scripts/run.sh"
    echo ""
fi

# Print access information
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                    FoamAgent is Ready!                         ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "🌐 Access the GUI in your web browser:"
echo "   http://localhost:6080"
echo ""
echo "📂 Save your cases in the 'work' directory"
echo ""
echo "📖 Documentation:"
echo "   • Quick Start:     QUICKSTART.md"
echo "   • Troubleshooting: TROUBLESHOOTING.md"
echo "   • Architecture:    ARCHITECTURE.md"
echo ""
echo "🔧 Useful commands:"
echo "   • View logs:       ./scripts/logs.sh"
echo "   • Stop container:  ./scripts/stop.sh"
echo "   • Access shell:    ./scripts/shell.sh"
echo ""
echo "Press Ctrl+C to stop viewing this message"
echo "The container will continue running in the background"
echo ""

# Open browser automatically (optional)
if command -v open &> /dev/null; then
    echo "Opening browser in 3 seconds..."
    sleep 3
    open http://localhost:6080
elif command -v xdg-open &> /dev/null; then
    echo "Opening browser in 3 seconds..."
    sleep 3
    xdg-open http://localhost:6080
fi
