# FoamAgent Project Summary

## What is FoamAgent?

FoamAgent is a modern, containerized Qt6 GUI application for managing OpenFOAM computational fluid dynamics (CFD) cases. It provides a complete web-based interface for:

- **Case Management**: Create, open, and manage OpenFOAM cases
- **Mesh Generation**: Run blockMesh, snappyHexMesh, and check mesh quality
- **Solver Execution**: Configure and run OpenFOAM solvers with real-time monitoring
- **Visualization**: Integrated ParaView support for results visualization
- **Web Access**: Access the full GUI from any modern web browser

## Key Features

### 1. Containerized Deployment
- Everything runs in a single Docker container
- Ubuntu 22.04 base with Qt6, OpenFOAM v2312, and ParaView
- No installation required on host machine (except Docker)
- Consistent environment across all platforms

### 2. Web-Based Access
- VNC server (TigerVNC) provides remote desktop
- noVNC enables browser-based access (no VNC client needed)
- Access from anywhere: `http://localhost:6080`
- Supports multiple concurrent users

### 3. Full Qt6 GUI
- Modern, responsive interface
- Tabbed workflow: Mesh → Solver → Visualization
- Real-time log output and progress monitoring
- Integrated help and status information

### 4. OpenFOAM Integration
- Automatic case structure creation
- Dictionary file generation
- Process execution and monitoring
- Template-based workflow support

### 5. Data Persistence
- `/work` directory mounted as volume
- Cases persist across container restarts
- Edit files from host or container
- Easy backup and version control

## Project Structure

```
FoamAgent/
├── README.md                    # Main project documentation
├── QUICKSTART.md               # Getting started guide
├── ARCHITECTURE.md             # Technical architecture
├── CONTRIBUTING.md             # Contribution guidelines
├── TROUBLESHOOTING.md          # Common issues and solutions
├── LICENSE                     # MIT License
├── Dockerfile                  # Main container definition
├── CMakeLists.txt             # Build configuration
├── .gitignore                 # Git ignore patterns
├── .dockerignore              # Docker ignore patterns
│
├── src/                       # C++ Source Code
│   ├── main.cpp              # Application entry point
│   ├── mainwindow.h/cpp      # Main window implementation
│   ├── casemanager.h/cpp     # Case management logic
│   ├── meshwidget.h/cpp      # Mesh generation UI
│   ├── solverwidget.h/cpp    # Solver control UI
│   ├── visualizationwidget.h/cpp  # Visualization UI
│   └── processrunner.h/cpp   # Process execution
│
├── ui/                        # Qt UI Files
│   └── mainwindow.ui         # Main window UI definition
│
├── docker/                    # Docker Configuration
│   ├── supervisord.conf      # Service management
│   ├── requirements.txt      # Python dependencies
│   ├── .env                  # Environment variables
│   └── scripts/              # Container scripts
│       └── start.sh          # Container startup
│
├── scripts/                   # Build and Run Scripts
│   ├── build.sh              # Build Docker container
│   ├── run.sh                # Run container
│   ├── dev.sh                # Development mode
│   ├── stop.sh               # Stop container
│   ├── logs.sh               # View logs
│   └── shell.sh              # Access container shell
│
├── examples/                  # Example Cases
│   └── templates/
│       └── cavity/           # Lid-driven cavity example
│           ├── README.md
│           └── blockMeshDict
│
└── work/                      # User Cases (mounted volume)
    └── README.md             # Work directory info
```

## Technology Stack

### Frontend Layer
- **Qt6**: Modern C++ GUI framework
- **Qt Widgets**: Native desktop UI components
- **Qt Charts**: Data visualization (future)

### Application Layer
- **C++17**: Modern C++ features
- **CMake**: Build system
- **Signal/Slots**: Event-driven architecture

### Integration Layer
- **QProcess**: External process management
- **File I/O**: OpenFOAM file handling
- **IPC**: Process communication

### Backend Layer
- **OpenFOAM v2312**: CFD solver suite
- **ParaView**: Scientific visualization
- **Python**: Automation scripts

### Infrastructure Layer
- **Docker**: Containerization
- **Ubuntu 22.04**: Linux base
- **TigerVNC**: VNC server
- **noVNC**: WebSocket VNC proxy
- **Xvfb**: Virtual display
- **supervisord**: Process manager

## Getting Started - Quick Commands

```bash
# Build the container (one time, 10-20 minutes)
./scripts/build.sh

# Run the application
./scripts/run.sh

# Access in browser
open http://localhost:6080

# View logs
./scripts/logs.sh

# Access container shell
./scripts/shell.sh

# Stop the application
./scripts/stop.sh

# Development mode (live code updates)
./scripts/dev.sh
```

## Typical Workflow

1. **Start Application**: `./scripts/run.sh`
2. **Open Browser**: Navigate to `http://localhost:6080`
3. **Create Case**: File → New Case → Select `/work/myCase`
4. **Configure Mesh**: Go to Mesh tab, set parameters, run blockMesh
5. **Setup Solver**: Go to Solver tab, select solver (e.g., icoFoam)
6. **Run Simulation**: Click "Run Solver", monitor progress
7. **Visualize Results**: Go to Visualization tab, launch ParaView
8. **Save & Exit**: Cases in `/work` are automatically persisted

## Use Cases

### Educational
- Teaching CFD fundamentals
- Demonstrating OpenFOAM workflows
- Hands-on training without complex installation

### Research
- Quick case setup and testing
- Reproducible computational environments
- Collaborative case development

### Industrial
- Prototype CFD analysis
- Pre-processing and post-processing
- Remote CFD workstation

### Development
- OpenFOAM case testing
- Solver development
- Automation script development

## Advantages

### For Users
- No complex installation or configuration
- Works on any OS with Docker (Mac, Windows, Linux)
- Access from anywhere via browser
- Visual interface for command-line tools
- Persistent case storage

### For Administrators
- Single container deployment
- No desktop environment required on server
- Easy scaling and deployment
- Consistent environment
- Simple backup and migration

### For Developers
- Clean separation of concerns
- Extensible architecture
- Standard Qt patterns
- Well-documented codebase
- Development mode for rapid iteration

## Future Enhancements

Potential areas for expansion:

1. **Advanced Visualization**
   - Embed VTK rendering directly in Qt
   - Real-time field plotting
   - Animation generation

2. **Parallel Computing**
   - MPI support for parallel solvers
   - Cluster integration
   - Job queue management

3. **Cloud Integration**
   - Remote storage (S3, Google Drive)
   - Cloud-based solving
   - Collaborative editing

4. **Enhanced Workflow**
   - Case wizards and templates
   - Automated parameter studies
   - Result comparison tools

5. **Web-Native UI**
   - React/Vue frontend
   - REST API backend
   - WebSocket for real-time updates
   - No VNC dependency

6. **Plugin System**
   - Custom solver integration
   - Third-party tools
   - Workflow extensions

## Performance Considerations

### Resource Requirements
- **Minimum**: 4GB RAM, 2 CPU cores, 10GB disk
- **Recommended**: 8GB RAM, 4 CPU cores, 50GB disk
- **Heavy CFD**: 16GB+ RAM, 8+ CPU cores, 100GB+ disk

### Optimization Tips
- Reduce VNC resolution for better performance
- Use volume mounts for large case data
- Increase Docker resources in settings
- Use parallel solvers for large meshes

## Security

- Container isolation provides security boundary
- No direct host access except mounted volumes
- VNC password protection (configurable)
- Can run behind reverse proxy with authentication
- No external network access required for operation

## Deployment Options

### Local Desktop
```bash
./scripts/run.sh
# Access at localhost:6080
```

### Remote Server
```bash
# On server
./scripts/run.sh

# From client browser
http://server-ip:6080
```

### Behind Reverse Proxy (NGINX)
```nginx
location /foamagent/ {
    proxy_pass http://localhost:6080/;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
```

## License

MIT License - See LICENSE file for details

## Support and Documentation

- **Quick Start**: QUICKSTART.md
- **Architecture**: ARCHITECTURE.md  
- **Troubleshooting**: TROUBLESHOOTING.md
- **Contributing**: CONTRIBUTING.md
- **OpenFOAM Docs**: https://www.openfoam.com/documentation
- **Qt6 Docs**: https://doc.qt.io/qt-6/

## Acknowledgments

This project builds upon:
- **OpenFOAM**: Open-source CFD toolkit
- **Qt**: Cross-platform application framework
- **ParaView**: Open-source visualization application
- **Docker**: Container platform
- **noVNC**: Browser-based VNC client

## Contact and Contribution

Contributions are welcome! See CONTRIBUTING.md for guidelines.

For questions, issues, or suggestions:
- Open a GitHub issue
- Check existing documentation
- Review troubleshooting guide

---

**Built with ❤️ for the CFD community**
