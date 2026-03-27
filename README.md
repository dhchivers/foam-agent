# FoamAgent - Qt6 OpenFOAM GUI with Web Interface

A containerized Qt6 application for setting up, running, and visualizing OpenFOAM cases, accessible through modern web browsers.

## Architecture

- **Qt6 GUI**: Native Qt6 C++ application for OpenFOAM case management
- **OpenFOAM**: CFD solver integrated within the container (v12)
- **Docker**: Ubuntu-based container with all dependencies
- **Web Access**: noVNC + TigerVNC for browser-based GUI access
- **Visualization**: ParaView integration for results visualization

> **Note:** Currently configured with OpenFOAM only for initial testing. Additional physics engines (Geant4, Newton, openEMS, OpenSim) will be enabled incrementally after verifying the core system.

## Features

- Interactive case setup and configuration
- Mesh generation and validation
- Solver execution and monitoring
- Real-time visualization of results
- Web-based access from any browser
- Case templates for common scenarios
- Extensible architecture for future multi-physics coupling

## Quick Start

### Build the Docker Container

```bash
./scripts/build.sh
```

### Run the Application

```bash
./scripts/run.sh
```

### Access via Web Browser

Open your browser and navigate to:
```
http://localhost:6080
```

## Project Structure

```
FoamAgent/
├── docker/
│   ├── Dockerfile              # Main container definition
│   ├── requirements.txt        # Python dependencies
│   └── scripts/                # Container startup scripts
├── src/
│   ├── main.cpp               # Application entry point
│   ├── mainwindow.cpp/h       # Main GUI window
│   ├── casemanager.cpp/h      # OpenFOAM case management
│   ├── meshwidget.cpp/h       # Mesh visualization
│   └── solverwidget.cpp/h     # Solver control panel
├── ui/
│   └── mainwindow.ui          # Qt Designer UI files
├── resources/
│   └── icons/                 # Application icons
├── scripts/
│   ├── build.sh              # Build container
│   ├── run.sh                # Run container
│   └── dev.sh                # Development mode
├── examples/
│   └── templates/            # OpenFOAM case templates
├── CMakeLists.txt            # Build configuration
└── README.md                 # This file
```

## Requirements

- Docker Engine 20.10+
- 4GB+ RAM
- Modern web browser (Chrome, Firefox, Safari, Edge)

## Development

### Local Development

For development with live code reload:

```bash
./scripts/dev.sh
```

### Building Outside Docker

If you have Qt6 and OpenFOAM installed locally:

```bash
mkdir build && cd build
cmake ..
make
./FoamAgent
```

## Configuration

Environment variables can be set in `docker/.env`:

- `VNC_PASSWORD`: Set VNC password (default: foamagent)
- `VNC_RESOLUTION`: Set display resolution (default: 1920x1080)
- `OPENFOAM_VERSION`: OpenFOAM version (default: v2312)

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in minutes
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment guide
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture and design
- **[MULTIPHYSICS.md](MULTIPHYSICS.md)** - Multi-physics coupling guide
- **[OPENEMS_GUIDE.md](OPENEMS_GUIDE.md)** - Electromagnetic simulation tutorial
- **[OPENSIM_GUIDE.md](OPENSIM_GUIDE.md)** - Biomechanical simulation tutorial
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Comprehensive project overview

## License

MIT License - See [LICENSE](LICENSE) for details

## Contributing

Contributions welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.
# foam-agent
# foam-agent
