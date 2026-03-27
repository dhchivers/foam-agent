# Architecture and Design

## System Architecture

FoamAgent is built as a multi-layered application with clear separation of concerns:

```
┌─────────────────────────────────────────┐
│         Web Browser Interface            │
│         (noVNC Client)                   │
└──────────────┬──────────────────────────┘
               │ WebSocket/HTTP
┌──────────────▼──────────────────────────┐
│         noVNC Server                     │
│         (websockify)                     │
└──────────────┬──────────────────────────┘
               │ VNC Protocol
┌──────────────▼──────────────────────────┐
│         VNC Server (TigerVNC)            │
│         X11 Display :1                   │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│         Qt6 Application Layer            │
│  ┌────────────────────────────────────┐ │
│  │      MainWindow                    │ │
│  │  ┌──────┬──────┬──────────────┐   │ │
│  │  │ Mesh │Solver│Visualization │   │ │
│  │  │Widget│Widget│   Widget     │   │ │
│  │  └──────┴──────┴──────────────┘   │ │
│  └────────────────────────────────────┘ │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│         Business Logic Layer             │
│  ┌────────────────┬──────────────────┐  │
│  │  CaseManager   │  ProcessRunner   │  │
│  └────────────────┴──────────────────┘  │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│         OpenFOAM Layer                   │
│         (blockMesh, solvers, etc.)       │
└──────────────────────────────────────────┘
```

## Component Details

### Qt6 Application Layer

**MainWindow**
- Central hub for the application
- Manages tabs and navigation
- Handles menu actions and file operations
- Coordinates between widgets

**MeshWidget**
- Mesh generation controls (blockMesh, snappyHexMesh)
- Mesh parameter configuration
- Quality checking interface
- Mesh import/export

**SolverWidget**
- Solver selection and configuration
- Execution controls
- Progress monitoring
- Real-time output display

**VisualizationWidget**
- ParaView integration
- Field and time step selection
- Visualization type control
- Quick preview capabilities

### Business Logic Layer

**CaseManager**
- OpenFOAM case lifecycle management
- File structure creation and validation
- Dictionary file generation
- Case metadata handling

**ProcessRunner**
- External process execution
- Output streaming
- Error handling
- Process lifecycle management

## Data Flow

### Case Creation Flow
```
User Action → MainWindow::newCase()
           → CaseManager::createNewCase()
           → Create directory structure
           → Generate dictionary files
           → Emit caseOpened signal
           → Update UI widgets
```

### Solver Execution Flow
```
User clicks "Run Solver"
           → SolverWidget::runSolver()
           → CaseManager::runSolver()
           → ProcessRunner::runCommand()
           → Stream output to UI
           → Monitor progress
           → Handle completion
```

## Communication Patterns

### Qt Signals and Slots

The application uses Qt's signal/slot mechanism for loose coupling:

```cpp
// CaseManager emits signals
emit statusMessage("Case opened");
emit logMessage("Running blockMesh...");

// Widgets connect to these signals
connect(caseManager, &CaseManager::logMessage, 
        logWidget, &QTextEdit::append);
```

### Process Communication

```
ProcessRunner → QProcess → OpenFOAM Tool
                   ↓
            stdout/stderr
                   ↓
      ProcessRunner signals
                   ↓
         Widget display
```

## Docker Container Architecture

The container runs multiple services managed by supervisord:

1. **Xvfb** - Virtual framebuffer (X11 display)
2. **VNC Server** - TigerVNC for remote desktop
3. **noVNC** - WebSocket-to-VNC proxy
4. **FoamAgent** - The Qt6 application

### Service Dependencies

```
Xvfb (Priority 100)
  ↓
VNC Server (Priority 200)
  ↓
noVNC (Priority 300)
  ↓
FoamAgent (Priority 400)
```

## File System Layout

### Container File System
```
/opt/openfoam2312/          # OpenFOAM installation
/app/                       # Application directory
  ├── build/               # Compiled binaries
  ├── src/                 # Source code
  └── ui/                  # UI files
/work/                      # User cases (mounted volume)
```

### Case Directory Structure
```
myCase/
  ├── 0/                   # Initial conditions
  ├── constant/            # Physical properties
  │   └── polyMesh/       # Mesh data
  ├── system/             # Simulation control
  │   ├── controlDict
  │   ├── fvSchemes
  │   └── fvSolution
  └── [time directories]  # Results
```

## Security Considerations

1. **Container Isolation**: Application runs in isolated Docker container
2. **Volume Mounting**: Only /work directory is accessible
3. **Network Exposure**: Only VNC ports exposed
4. **No Root Access**: Application runs as root in container (isolated)

## Performance Considerations

1. **Shared Memory**: Container uses --shm-size=2g for X11 performance
2. **Process Streaming**: Output streamed line-by-line to prevent blocking
3. **Qt Signals**: Asynchronous communication prevents UI freezing
4. **Volume Mounting**: Direct host filesystem access for case data

## Extension Points

### Adding New Solvers
1. Add solver name to `CaseManager::getAvailableSolvers()`
2. Add description in `SolverWidget::selectSolver()`
3. Optionally add solver-specific UI elements

### Adding New Mesh Tools
1. Create new methods in `CaseManager`
2. Add buttons/controls in `MeshWidget`
3. Connect signals for process execution

### Custom Visualization
1. Extend `VisualizationWidget`
2. Add VTK/rendering integration
3. Create custom view controls

## Future Enhancements

- **Web-based UI**: Replace Qt with web frontend using WebAssembly or REST API
- **Parallel Computing**: Support for mpirun and parallel solvers
- **Remote Cases**: SSH/cloud storage integration
- **Collaboration**: Multi-user case editing
- **Plugins**: Plugin system for custom solvers and workflows
