#!/bin/bash
# Access a shell inside the running FoamAgent container

CONTAINER_NAME="${CONTAINER_NAME:-foamagent}"

if [ ! "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
    echo "Container $CONTAINER_NAME is not running"
    echo "Start it with: ./scripts/run.sh"
    exit 1
fi

echo "Entering container shell..."
echo "OpenFOAM and Geant4 environments will be loaded automatically"
echo "(Newton, openEMS, and OpenSim temporarily disabled - will be re-enabled after debugging)"
echo "Exit with 'exit' or Ctrl+D"
echo ""

docker exec -it $CONTAINER_NAME bash -c "source /opt/openfoam12/etc/bashrc && source /opt/geant4/bin/geant4.sh && bash"
