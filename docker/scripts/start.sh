#!/bin/bash
# Startup script for container services

# Source OpenFOAM environment
source /opt/openfoam12/etc/bashrc

# Source Geant4 environment
source /opt/geant4/bin/geant4.sh

# Set openEMS environment
export PATH=/opt/openEMS/bin:$PATH
export LD_LIBRARY_PATH=/opt/openEMS/lib:$LD_LIBRARY_PATH

# Set OpenSim environment
export PATH=/opt/opensim/bin:$PATH
export LD_LIBRARY_PATH=/opt/opensim/lib:$LD_LIBRARY_PATH

# Create log directory
mkdir -p /var/log/supervisor

# Start supervisor
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
