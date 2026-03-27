# FoamAgent Quick Start Guide

## Installation

### Prerequisites
- Docker Engine 20.10 or later
- Minimum 4GB RAM
- Modern web browser

### Build and Run

1. **Clone or download the project**
   ```bash
   cd /Users/chivers/FoamAgent
   ```

2. **Build the Docker container**
   ```bash
   ./scripts/build.sh
   ```
   This will take 10-20 minutes on first build as it downloads and installs:
   - Ubuntu 22.04
   - Qt6 libraries
   - OpenFOAM v2312
   - ParaView
   - VNC server components

3. **Run the application**
   ```bash
   ./scripts/run.sh
   ```

4. **Access the GUI**
   Open your browser and navigate to:
   ```
   http://localhost:6080
   ```

## First Steps

### Creating Your First Case

1. **Click "New Case"** in the File menu
2. **Select a directory** (use `/work` for persistent storage)
3. **Enter a case name** (e.g., "myFirstCase")

The application will create a standard OpenFOAM case structure:
```
myFirstCase/
├── 0/         # Initial conditions
├── constant/  # Physical properties
└── system/    # Solver settings
```

### Generating a Mesh

1. **Go to the "Mesh Generation" tab**
2. **Configure mesh parameters**:
   - Cells in X: 20
   - Cells in Y: 20
   - Cells in Z: 1 (for 2D cases)
3. **Click "Run blockMesh"**
4. **Monitor progress** in the log window

### Running a Simulation

1. **Go to the "Solver Setup" tab**
2. **Select a solver** (start with "icoFoam" for simple cases)
3. **Click "Run Solver"**
4. **Watch progress** in the solver output window

### Visualizing Results

1. **Go to the "Visualization" tab**
2. **Click "Launch ParaView"**
   
   OR
   
   **Use the built-in quick view**:
   - Select time step
   - Choose field (U, p, T, etc.)
   - Select visualization type

## Common Workflows

### Workflow 1: Cavity Flow Tutorial

The classic lid-driven cavity case:

1. **Create new case** named "cavity"
2. **Copy template files**:
   - Use the example template in `examples/templates/cavity/`
3. **Generate mesh**: Run blockMesh
4. **Run simulation**: Select icoFoam
5. **Visualize**: Launch ParaView when complete

### Workflow 2: Custom Geometry

For custom geometries:

1. **Create case**
2. **Prepare geometry** (STL file)
3. **Use snappyHexMesh**:
   - Place STL in `constant/triSurface/`
   - Configure snappyHexMeshDict
   - Run snappyHexMesh
4. **Set boundary conditions**
5. **Run solver**

## Tips and Tricks

### Keyboard Shortcuts
- `Ctrl+N` - New Case
- `Ctrl+O` - Open Case
- `Ctrl+S` - Save Case
- `Ctrl+Q` - Quit

### Working Directory
- Cases saved in `/work` inside the container
- This maps to `FoamAgent/work` on your host machine
- Files persist between container restarts

### Performance
- Use `./scripts/run.sh` for normal operation
- Use `./scripts/dev.sh` for development with live code updates
- Adjust VNC resolution: `VNC_RESOLUTION=1280x720 ./scripts/run.sh`

### Logs and Debugging
- View container logs: `docker logs -f foamagent`
- Check specific service: `docker exec -it foamagent supervisorctl status`
- Access container shell: `docker exec -it foamagent bash`

## Stopping and Starting

### Stop the Application
```bash
docker stop foamagent
```

### Restart the Application
```bash
docker start foamagent
```
Access at http://localhost:6080 again

### Remove the Container
```bash
docker stop foamagent
docker rm foamagent
```

## Next Steps

- Explore the example templates in `examples/templates/`
- Read the [OpenFOAM User Guide](https://www.openfoam.com/documentation/user-guide)
- Check [ARCHITECTURE.md](ARCHITECTURE.md) for system design details
- See [CONTRIBUTING.md](CONTRIBUTING.md) if you want to extend FoamAgent

## Getting Help

- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues
- Review OpenFOAM documentation for solver-specific questions
- Open an issue on GitHub for bugs or feature requests

## Additional Resources

- **OpenFOAM**: https://www.openfoam.com
- **ParaView**: https://www.paraview.org
- **Qt Documentation**: https://doc.qt.io/qt-6/
