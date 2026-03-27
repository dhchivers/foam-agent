# openEMS Quick Start Guide

## Introduction

openEMS is an electromagnetic field solver using the FDTD (Finite-Difference Time-Domain) method. It's controlled via Octave/Matlab scripts.

## Accessing openEMS

```bash
# Access container shell
./scripts/shell.sh

# Start Octave
octave

# In Octave, the openEMS paths are automatically loaded
```

## Running Your First Simulation

### Example 1: Simple Antenna

```octave
% Navigate to tutorials
cd ~/openEMS/matlab/Tutorials

% Run a simple patch antenna example
Patch_Antenna

% This will:
% 1. Create the geometry
% 2. Run the FDTD simulation
% 3. Generate results and plots
```

### Example 2: Microstrip Line

```octave
cd ~/openEMS/matlab/Tutorials
MSL_NotchFilter
```

## Basic openEMS Workflow

### 1. Setup Geometry (using CSXCAD)

```octave
% Physical constants
physical_constants;

% Simulation parameters
f0 = 2e9;  % center frequency
fc = 1e9;  % cutoff frequency

% Initialize CSXCAD
CSX = InitCSX();

% Define mesh
mesh.x = [-100:5:100];
mesh.y = [-100:5:100];
mesh.z = [-50:2:50];
CSX = DefineRectGrid(CSX, unit, mesh);

% Add metal
CSX = AddMetal(CSX, 'metal');
CSX = AddBox(CSX, 'metal', 0, [0 0 0], [10 10 1]);
```

### 2. Define Excitation and Boundaries

```octave
% Add lumped port
start = [0 0 0];
stop  = [0 0 10];
[CSX port] = AddLumpedPort(CSX, 10, 1, 50, start, stop, [0 0 1], true);

% Add PML boundaries
CSX = AddPML(CSX, 8);
```

### 3. Run Simulation

```octave
% Write XML file
WriteOpenEMS('/tmp/mySimulation/geometry.xml', FDTD, CSX);

% Run openEMS
RunOpenEMS('/tmp/mySimulation', 'geometry.xml');
```

### 4. Post-Processing

```octave
% Read port data
port = calcPort(port, '/tmp/mySimulation/');

% Plot S-parameters
figure
plot(port.f/1e9, 20*log10(abs(port.uf.ref./port.uf.inc)));
xlabel('Frequency (GHz)');
ylabel('S11 (dB)');
grid on;
```

## Visualization

openEMS includes AppCSXCAD for 3D geometry visualization:

```bash
# View geometry before simulation
AppCSXCAD geometry.xml

# View fields after simulation (if VTK export enabled)
paraview field_data.vtk
```

## Common Applications

### RF/Microwave Circuits
- Filters, couplers, power dividers
- Transmission lines
- Matching networks

### Antennas
- Patch antennas
- Dipoles, monopoles
- Arrays
- Horn antennas

### EMC/EMI
- Shielding effectiveness
- Crosstalk analysis
- Radiated emissions

## Integration with Other Tools

### Export to ParaView

```octave
% Enable VTK dump in simulation
FDTD = SetGaussExcite(FDTD, f0, fc);
FDTD = SetBoundaryCond(FDTD, {'PML_8' 'PML_8' 'PML_8' 'PML_8' 'PML_8' 'PML_8'});

% Add field dump
CSX = AddDump(CSX, 'Et', 'FileType', 1);  % 1 = VTK
CSX = AddBox(CSX, 'Et', 0, start, stop);
```

### Coupling with OpenFOAM

For electromagnetic heating problems:

1. **Run openEMS** to get power dissipation
2. **Export power density** to file
3. **Import to OpenFOAM** as heat source
4. **Run thermal simulation**

Example power extraction:

```octave
% Get power dissipation field
P_loss = ReadHDF5Dump('/tmp/simulation/', 'power_loss');

% Export to format readable by OpenFOAM
% (requires custom export function)
exportToOpenFOAM(P_loss, 'power_source.dat');
```

## Tips and Best Practices

### Meshing
- Start with coarse mesh, refine gradually
- Use λ/20 resolution minimum (λ/10 for better accuracy)
- Refine mesh at material boundaries
- Use graded meshes to save memory

### Boundaries
- Use PML (Perfectly Matched Layer) for open boundaries
- Typically 8-10 layers sufficient
- PMC/PEC for symmetric boundaries

### Excitation
- Use Gaussian excitation for broadband
- Sine excitation for narrow band
- Plane wave for far-field problems

### Memory Management
- FDTD memory = Nx × Ny × Nz × 6 fields × 8 bytes
- Example: 100×100×100 mesh ≈ 480 MB
- Large simulations may need >8GB RAM

### Simulation Time
- FDTD time steps limited by stability (CFL condition)
- Smaller cells → more time steps
- Use `--numThreads=N` for parallel execution

## Troubleshooting

### Simulation doesn't converge
- Check excitation amplitude
- Verify boundary conditions
- Ensure proper meshing at interfaces

### Memory errors
- Reduce mesh size
- Use coarser resolution
- Enable data compression

### Unstable results
- Check CFL stability condition
- Reduce time step if needed
- Verify material properties

## Advanced Topics

### Custom Materials

```octave
% Define dielectric
CSX = AddMaterial(CSX, 'substrate');
CSX = SetMaterialProperty(CSX, 'substrate', 'Epsilon', 4.3, 'Kappa', 0.001);

% Add lossy metal
CSX = AddConductingSheet(CSX, 'copper', 56e6, 35e-6);
```

### Periodic Boundaries

```octave
% For antenna arrays or FSS
FDTD = SetBoundaryCond(FDTD, {'PBC' 'PBC' 'PML_8' 'PML_8' 'MUR' 'MUR'});
```

### Far-Field Calculation

```octave
% Add NF2FF box
start_nf2ff = [mesh.x(1) mesh.y(1) mesh.z(1)];
stop_nf2ff  = [mesh.x(end) mesh.y(end) mesh.z(end)];
[CSX nf2ff] = CreateNF2FFBox(CSX, 'nf2ff', start_nf2ff, stop_nf2ff);

% After simulation, calculate far-field
nf2ff = CalcNF2FF(nf2ff, '/tmp/simulation/', f0);

% Plot pattern
plotFF3D(nf2ff);
```

## Example: Complete Dipole Antenna

```octave
close all
clear
clc

physical_constants;

% Parameters
f0 = 1e9;           % 1 GHz
lambda = c0/f0;     % wavelength
length = lambda/2;  % dipole length

% Setup FDTD
FDTD = InitFDTD('NrTS', 30000);
FDTD = SetGaussExcite(FDTD, f0, f0/2);
BC = {'MUR' 'MUR' 'MUR' 'MUR' 'MUR' 'MUR'};
FDTD = SetBoundaryCond(FDTD, BC);

% Setup CSXCAD geometry
CSX = InitCSX();

% Create mesh
mesh_res = lambda/20;
mesh.x = -lambda:mesh_res:lambda;
mesh.y = -lambda:mesh_res:lambda;
mesh.z = -lambda:mesh_res:lambda;
CSX = DefineRectGrid(CSX, 1, mesh);

% Create dipole
CSX = AddMetal(CSX, 'dipole');
start = [0 0 -length/2];
stop  = [0 0  length/2];
CSX = AddCylinder(CSX, 'dipole', 10, start, stop, lambda/100);

% Add excitation
[CSX port] = AddLumpedPort(CSX, 1, 0, 50, ...
    [-lambda/100 -lambda/100 -mesh_res], ...
    [ lambda/100  lambda/100  mesh_res], [0 0 1], true);

% Write and run
Sim_Path = '/tmp/dipole';
Sim_CSX = 'dipole.xml';
mkdir(Sim_Path);
WriteOpenEMS([Sim_Path '/' Sim_CSX], FDTD, CSX);
RunOpenEMS(Sim_Path, Sim_CSX);

% Post-processing
port = calcPort(port, Sim_Path);

% Plot results
figure
plot(port.f/1e9, 20*log10(abs(port.uf.ref./port.uf.inc)));
xlabel('Frequency (GHz)');
ylabel('|S11| (dB)');
title('Dipole Antenna Reflection Coefficient');
grid on;
```

## Resources

- **Documentation**: https://openems.de/index.php/Documentation
- **Tutorials**: `~/openEMS/matlab/Tutorials`
- **Forum**: https://openems.de/forum/
- **Examples**: Check the Tutorials directory for many more examples

## Next Steps

1. Work through tutorials in `~/openEMS/matlab/Tutorials`
2. Modify examples for your specific needs
3. Explore coupling with other simulation tools
4. Check the openEMS documentation for advanced features

Happy simulating! 📡
