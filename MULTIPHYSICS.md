# Multi-Physics Simulation Guide

## Overview

FoamAgent currently includes two major simulation engines, with more to be added:

1. **OpenFOAM v12** - Computational Fluid Dynamics (CFD)
2. **Geant4 v11.4.1** - Monte Carlo Particle Physics Simulation

**Temporarily Disabled (will be re-enabled):**
- Newton Dynamics - Rigid body physics (build configuration issues)
- openEMS - Electromagnetic FDTD (dependency build issues)
- OpenSim v4.5.1 - Biomechanics (disabled to speed up initial build)

## Installed Components

### OpenFOAM v12
- **Location**: `/opt/openfoam12`
- **Environment**: Automatically sourced in shell
- **Installation**: Official packaged version
- **Use cases**: Fluid flow, heat transfer, turbulence, multiphase flows

### Newton Dynamics (TEMPORARILY DISABLED)
- **Status**: Build issues - will be re-enabled once resolved
- **Planned Location**: `/usr/local`
- **Use cases**: Rigid body collisions, joints, constraints, mechanical systems

### openEMS (TEMPORARILY DISABLED)
- **Status**: CSXCAD dependency build issues - will be re-enabled once resolved
- **Planned Location**: `/opt/openEMS`
- **Interface**: Octave/Matlab scripts
- **Use cases**: Electromagnetic field simulation, antenna design, RF/microwave circuits, EMC/EMI

### OpenSim (TEMPORARILY DISABLED)
- **Status**: Disabled to speed up initial build - will be enabled after core verification
- **Planned Location**: `/opt/opensim`
- **Components**: SimBody multibody dynamics engine
- **Use cases**: Musculoskeletal modeling, biomechanics, motion analysis, muscle force prediction

### Geant4 v11.4.1
- **Location**: `/opt/geant4`
- **Environment**: Automatically sourced in shell
- **Data files**: Automatically downloaded during build
- **Use cases**: Particle transport, radiation simulation, detector response, medical physics

## Verification

After building the container, verify components:

```bash
# Access container shell
./scripts/shell.sh

# Check OpenFOAM
which icoFoam
foamVersion

# Check Geant4
which geant4-config
geant4-config --version
geant4-config --libs
echo $G4INSTALL
```

## Multi-Physics Use Cases

### 1. Particle Transport Through Fluids
**Combination**: Geant4 + OpenFOAM

Example workflow:
- Use OpenFOAM to simulate fluid flow
- Export velocity field
- Use Geant4 to track particles through the fluid field
- Account for fluid drag and dispersion

### 2. Fluid-Structure Interaction
**Combination**: OpenFOAM + Newton Dynamics

Example workflow:
- Use OpenFOAM for fluid forces
- Use Newton Dynamics for rigid body response
- Couple forces and displacements iteratively

### 3. Radiation Effects on Fluid Systems
**Combination**: Geant4 + OpenFOAM

Example workflow:
- Use Geant4 to simulate radiation energy deposition
- Use deposited energy as heat source in OpenFOAM
- Simulate thermal-hydraulic response

### 4. Biomechanical Fluid-Structure Interaction
**Combination**: OpenSim + OpenFOAM

Example workflow:
- Use OpenSim to simulate musculoskeletal motion
- Export vessel/organ wall deformation
- Use deformation as moving boundary in OpenFOAM
- Simulate biofluid dynamics (blood flow, respiration)
- Couple flow forces back to OpenSim

### 5. Complete Multi-Physics
**Combination**: All five engines

Example: Nuclear reactor simulation
- Geant4: Neutron/gamma transport
- OpenFOAM: Coolant flow and heat transfer
- Newton Dynamics: Control rod mechanics
- openEMS: Electromagnetic interference/compatibility
- OpenSim: Human operator ergonomics/safety analysis

### 6. Electromagnetic-Thermal Coupling
**Combination**: openEMS + OpenFOAM

Example workflow:
- Use openEMS to simulate RF heating
- Extract power dissipation field
- Use as heat source in OpenFOAM
- Simulate thermal management

### 7. Electromagnetic-Particle Coupling
**Combination**: openEMS + Geant4

Example workflow:
- Use openEMS for RF/microwave fields
- Export electromagnetic field distribution
- Use in Geant4 for charged particle tracking
- Particle accelerator design

## Data Exchange

### File-Based Coupling

Most common approach for loose coupling:

```bash
# OpenFOAM exports data
foamToVTK
postProcess -func writeCellCentres

# Read in custom code
# Process with Geant4/Newton
# Write results back

# Import to OpenFOAM
mapFields
```

### API-Based Coupling

For tight coupling, you can:

1. **Link libraries** in custom solvers
2. **Use shared memory** for data exchange
3. **Implement coupling interfaces**

Example CMake for coupled code:

```cmake
find_package(Geant4 REQUIRED)
find_package(Newton REQUIRED)

# Your custom solver
add_executable(coupledSolver main.cpp)
target_link_libraries(coupledSolver
    ${OPENFOAM_LIBRARIES}
    ${Geant4_LIBRARIES}
    newton
)
```

## Environment Setup

All environments are automatically loaded when you access the shell:

```bash
./scripts/shell.sh
```

This sources:
- OpenFOAM: `/opt/openfoam12/etc/bashrc`
- Geant4: `/opt/geant4/bin/geant4.sh`

## Example: Simple Multi-Physics Workflow

### Step 1: Create OpenFOAM Case
```bash
cd /work
cp -r $FOAM_TUTORIALS/incompressible/icoFoam/cavity/cavity myCase
cd myCase
blockMesh
icoFoam
```

### Step 2: Extract Results
```bash
# Export to VTK for visualization
foamToVTK

# Or write specific fields
postProcess -func 'writeObjects(U,p)'
```

### Step 3: Use in Geant4
Create a Geant4 application that:
- Reads OpenFOAM mesh
- Uses velocity field for particle transport
- Outputs particle trajectories

### Step 4: Use in Newton Dynamics
- Read forces from fluid
- Apply to rigid bodies
- Compute motion
- Update boundary conditions in OpenFOAM

## Development Tips

### Compiling Custom Multi-Physics Code

```bash
# Inside container
cd /work/myMultiPhysicsCode

# CMakeLists.txt should find all three
find_package(OpenFOAM REQUIRED)
find_package(Geant4 REQUIRED)
find_package(Newton REQUIRED)

# Build
mkdir build && cd build
cmake ..
make
```

### Debugging

```bash
# Check library paths
echo $LD_LIBRARY_PATH

# Check if libraries are found
ldd ./myExecutable

# Geant4 debugging
export G4DEBUG=1

# OpenFOAM debugging
export FOAM_ABORT=1
```

## Performance Considerations

### Memory Requirements
- **Minimum**: 8GB RAM
- **Recommended**: 16GB+ RAM
- **Large simulations**: 32GB+ RAM

### CPU Usage
- Both engines support parallel execution
- OpenFOAM: Use `mpirun` for parallel solvers
- Geant4: Built with multithreading support

### Disk Space
- OpenFOAM: ~1.5GB (packaged install)
- Geant4 (with data): ~5GB
- **Total**: ~7GB for base installation
- **Cases**: 1-100GB+ depending on mesh size and time steps

## Example Applications

### Medical Physics / Bioengineering
- **OpenSim**: Musculoskeletal dynamics, gait analysis
- **OpenFOAM**: Blood flow, respiratory mechanics
- **Geant4**: Radiation dose calculation, medical imaging
- **openEMS**: Medical device RF/EM analysis
- **Newton**: Surgical tool dynamics

### Nuclear Engineering
- **Geant4**: Neutron/gamma transport
- **OpenFOAM**: Reactor thermal-hydraulics
- **Newton**: Control mechanism dynamics

### Environmental Science
- **Geant4**: Cosmic ray propagation
- **OpenFOAM**: Atmospheric flow
- **Newton**: Debris tracking

### Aerospace
- **Geant4**: Radiation environment
- **OpenFOAM**: Aerodynamics
- **Newton**: Spacecraft dynamics
- **openEMS**: Antenna design, RF communication

### Electronics Cooling
- **openEMS**: EMI/EMC analysis
- **OpenFOAM**: Thermal management
- **Newton**: Mechanical vibration

### Sports Science / Human Performance
- **OpenSim**: Athlete biomechanics, injury prediction
- **OpenFOAM**: Aerodynamics (cycling, swimming)
- **Newton**: Equipment dynamics (ball trajectories)
- **Geant4**: Radiation exposure (high altitude)

- **openEMS**: https://openems.de/start/index.php
- **OpenSim**: https://simtk-confluence.stanford.edu/display/OpenSim/Documentation

### Tutorials
- OpenFOAM tutorials: `$FOAM_TUTORIALS`
- Geant4 examples: `$G4INSTALL/share/Geant4/examples`
- Newton examples: In source repository
- openEMS tutorials: `~/openEMS/matlab/Tutorials`
- OpenSim examples: `/opt/opensim/Resources/Models`

## Resources

### Documentation
- **OpenFOAM**: https://www.openfoam.com/documentation
- **Geant4**: https://geant4.web.cern.ch/support/user_documentation
- **Newton Dynamics**: https://github.com/MADEAPPS/newton-dynamics

### Tutorials
- OpenFOAM tutorials: `$FOAM_TUTORIALS`
- Geant4 examples: `$G4INSTALL/share/Geant4/examples`
- Newton examples: In source repository
- openEMS tutorials: `~/openEMS/matlab/Tutorials`
- OpenSim examples: `/opt/opensim/Resources/Models`

### Community
- OpenFOAM Forum: https://www.cfd-online.com/Forums/openfoam/
- Geant4 Forum: https://geant4-forum.web.cern.ch/
- Newton Discord: Check GitHub repository
- openEMS Forum: https://openems.de/forum/
- OpenSim Forum: https://simtk.org/forums/viewforum.php?f=91

## Troubleshooting

### Libraries Not Found
```bash
# Geant4 libraries
export LD_LIBRARY_PATH=/opt/geant4/lib:$LD_LIBRARY_PATH

# Newton libraries
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

# Reload
ldconfig
```

### Environment Not Loaded
```bash
# Manually source environments
source /opt/openfoam12/etc/bashrc
source /opt/geant4/bin/geant4.sh
```

### Geant4 Data Files
If data files are missing:
```bash
# Download separately
cd /opt/geant4/share/Geant4/data
geant4-config --install-datasets
```

## Next Steps

1. **Learn each engine individually** - Master basics before coupling
2. **Start with simple coupling** - File-based coupling first
3. **Develop custom interfaces** - Create your own coupling code
4. **Optimize performance** - Profile and parallelize
5. **Validate results** - Compare with experimental data

## Support

For multi-physics simulation questions:
- Check individual tool documentation first
- Consult coupling examples in literature
- Community forums for specific tools
- Consider consulting services for complex coupling

---

**Happy Multi-Physics Simulating! 🚀**
