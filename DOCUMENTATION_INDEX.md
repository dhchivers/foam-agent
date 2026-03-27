# FoamAgent Documentation Index

Welcome to the FoamAgent documentation! This index helps you find the right information quickly.

## 📚 Complete Documentation Set

### Getting Started
1. **[README.md](README.md)** - Project overview and features
2. **[QUICKSTART.md](QUICKSTART.md)** - Get up and running in 5 minutes
3. **[start.sh](start.sh)** - Automated setup script

### Deployment
4. **[DEPLOYMENT.md](DEPLOYMENT.md)** - Complete deployment guide
   - Local development
   - Production servers
   - Cloud deployment (AWS/GCP/Azure)
   - Scaling and load balancing
   - Security hardening
   - Backup strategies

### Architecture & Design
5. **[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical architecture
   - System components
   - Data flow diagrams
   - Communication patterns
   - Extension points

6. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Comprehensive overview
   - Technology stack
   - Use cases
   - Future enhancements

7. **[MULTIPHYSICS.md](MULTIPHYSICS.md)** - Multi-physics simulation guide
   - OpenFOAM + Newton Dynamics + Geant4 + openEMS + OpenSim
   - Coupling strategies
   - Example workflows
   - Performance considerations

8. **[OPENEMS_GUIDE.md](OPENEMS_GUIDE.md)** - openEMS electromagnetic simulation
   - Getting started with FDTD
   - Antenna and RF circuit design
   - Integration with other tools
   - Complete examples

9. **[OPENSIM_GUIDE.md](OPENSIM_GUIDE.md)** - OpenSim biomechanical simulation
   - Musculoskeletal modeling
   - Motion analysis and inverse kinematics
   - Muscle force prediction
   - Biofluid coupling examples

### Problem Solving
10. **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Solutions to common issues
   - Build problems
   - Runtime errors
   - Performance issues
   - Data persistence

### Development
11. **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines
   - Development setup
   - Coding standards
   - Submitting changes
   - Testing procedures

### Scripts & Tools
12. **[scripts/README.md](scripts/README.md)** - Build and run scripts
   - build.sh - Build Docker image
   - run.sh - Start application
   - dev.sh - Development mode
   - stop.sh - Stop container
   - logs.sh - View logs
   - shell.sh - Access container

### Examples
13. **[examples/templates/cavity/README.md](examples/templates/cavity/README.md)** - Tutorial cases
    - Lid-driven cavity flow
    - Mesh configuration
    - Solver setup

### Reference
14. **[work/README.md](work/README.md)** - Working directory guide
15. **[LICENSE](LICENSE)** - MIT License terms

---

## 🎯 Find What You Need

### I want to...

**Get started quickly**
→ [QUICKSTART.md](QUICKSTART.md)

**Deploy to production**
→ [DEPLOYMENT.md](DEPLOYMENT.md)

**Understand how it works**
→ [ARCHITECTURE.md](ARCHITECTURE.md)

**Fix a problem**
→ [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

**Contribute code**
→ [CONTRIBUTING.md](CONTRIBUTING.md)

**Learn about the project**
→ [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

**Build and run**
→ [scripts/README.md](scripts/README.md)

**See examples**
→ [examples/templates/](examples/templates/)

---

## 📋 Quick Reference

### Common Commands

```bash
# First time setup
./start.sh                    # Automated setup and launch

# Manual control
./scripts/build.sh            # Build container
./scripts/run.sh              # Run application
./scripts/stop.sh             # Stop application
./scripts/logs.sh             # View logs
./scripts/shell.sh            # Access shell

# Using Make
make build                    # Build
make run                      # Run
make stop                     # Stop
make help                     # Show all commands
```

### Access Points

- **Web GUI**: http://localhost:6080
- **VNC Direct**: vnc://localhost:5901
- **Work Directory**: `/Users/chivers/FoamAgent/work`
- **Container Shell**: `./scripts/shell.sh`

### Key Directories

```
FoamAgent/
├── src/              # C++ source code
├── ui/               # Qt UI files
├── docker/           # Docker configuration
├── scripts/          # Build and run scripts
├── examples/         # Example cases
└── work/            # Your OpenFOAM cases (mounted volume)
```

---

## 📖 Reading Paths

### For New Users
1. [README.md](README.md) - Understand what FoamAgent is
2. [QUICKSTART.md](QUICKSTART.md) - Install and run
3. [examples/templates/](examples/templates/) - Try tutorial cases
4. [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - If you hit issues

### For System Administrators
1. [DEPLOYMENT.md](DEPLOYMENT.md) - Production deployment
2. [ARCHITECTURE.md](ARCHITECTURE.md) - System design
3. [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Operations guide
4. [scripts/README.md](scripts/README.md) - Automation scripts

### For Developers
1. [ARCHITECTURE.md](ARCHITECTURE.md) - System design
2. [CONTRIBUTING.md](CONTRIBUTING.md) - Development workflow
3. [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Technology stack
4. [scripts/README.md](scripts/README.md) - Development tools

### For Researchers/Engineers
1. [QUICKSTART.md](QUICKSTART.md) - Quick setup
2. [examples/templates/](examples/templates/) - Case templates
3. [README.md](README.md) - Feature overview
4. [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Problem solving

### For Multi-Physics Users
1. [MULTIPHYSICS.md](MULTIPHYSICS.md) - Coupled simulation guide
2. [OPENEMS_GUIDE.md](OPENEMS_GUIDE.md) - Electromagnetics
3. [OPENSIM_GUIDE.md](OPENSIM_GUIDE.md) - Biomechanics
4. [ARCHITECTURE.md](ARCHITECTURE.md) - System integration

---

## 🔍 Documentation by Topic

### Installation & Setup
- Quick: [QUICKSTART.md](QUICKSTART.md)
- Production: [DEPLOYMENT.md](DEPLOYMENT.md) → Production Server
- Cloud: [DEPLOYMENT.md](DEPLOYMENT.md) → Cloud Deployment
- Development: [CONTRIBUTING.md](CONTRIBUTING.md) → Development Setup

### Configuration
- Environment Variables: [DEPLOYMENT.md](DEPLOYMENT.md)
- VNC Settings: [README.md](README.md) → Configuration
- Docker Options: [scripts/README.md](scripts/README.md)

### Usage
- Creating Cases: [QUICKSTART.md](QUICKSTART.md) → Creating Your First Case
- Mesh Generation: [QUICKSTART.md](QUICKSTART.md) → Generating a Mesh
- Running Solvers: [QUICKSTART.md](QUICKSTART.md) → Running a Simulation
- Visualization: [QUICKSTART.md](QUICKSTART.md) → Visualizing Results

### Multi-Physics Simulation
- Overview: [MULTIPHYSICS.md](MULTIPHYSICS.md) → Overview
- Electromagnetics: [OPENEMS_GUIDE.md](OPENEMS_GUIDE.md)
- Biomechanics: [OPENSIM_GUIDE.md](OPENSIM_GUIDE.md)
- Coupling Strategies: [MULTIPHYSICS.md](MULTIPHYSICS.md) → Data Exchange
- Example Workflows: [MULTIPHYSICS.md](MULTIPHYSICS.md) → Use Cases

### Technical Details
- System Architecture: [ARCHITECTURE.md](ARCHITECTURE.md)
- Data Flow: [ARCHITECTURE.md](ARCHITECTURE.md) → Data Flow
- Component Details: [ARCHITECTURE.md](ARCHITECTURE.md) → Component Details
- Technology Stack: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) → Technology Stack

### Operations
- Monitoring: [DEPLOYMENT.md](DEPLOYMENT.md) → Monitoring
- Backups: [DEPLOYMENT.md](DEPLOYMENT.md) → Backup
- Security: [DEPLOYMENT.md](DEPLOYMENT.md) → Security
- Scaling: [DEPLOYMENT.md](DEPLOYMENT.md) → Scaling

### Troubleshooting
- Build Issues: [TROUBLESHOOTING.md](TROUBLESHOOTING.md) → Build Issues
- Runtime Issues: [TROUBLESHOOTING.md](TROUBLESHOOTING.md) → Runtime Issues
- Performance: [TROUBLESHOOTING.md](TROUBLESHOOTING.md) → Performance Issues
- Networking: [TROUBLESHOOTING.md](TROUBLESHOOTING.md) → Network Connectivity

### Development
- Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
- Code Style: [CONTRIBUTING.md](CONTRIBUTING.md) → Coding Standards
- Dev Mode: [scripts/README.md](scripts/README.md) → dev.sh
- Architecture: [ARCHITECTURE.md](ARCHITECTURE.md) → Extension Points

---

## 📞 Getting Help

### Self-Service
1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Review relevant documentation section above
3. Search existing issues on GitHub
4. Check OpenFOAM documentation for solver-specific questions

### Community Support
- GitHub Issues: Report bugs or request features
- GitHub Discussions: Ask questions and share experiences
- Stack Overflow: Tag with `openfoam` and `qt6`

### Professional Support
Contact the maintainers for:
- Enterprise deployment assistance
- Custom feature development
- Training and consultation
- Priority bug fixes

---

## 🎓 Learning Resources

### OpenFOAM
- [OpenFOAM User Guide](https://www.openfoam.com/documentation/user-guide)
- [OpenFOAM Tutorials](https://www.openfoam.com/documentation/tutorial-guide)
- [CFD Online Forums](https://www.cfd-online.com/Forums/openfoam/)

### Qt Development
- [Qt Documentation](https://doc.qt.io/qt-6/)
- [Qt Widgets Examples](https://doc.qt.io/qt-6/qtwidgets-examples.html)
- [Qt for Beginners](https://doc.qt.io/qt-6/gettingstarted.html)

### Docker
- [Docker Documentation](https://docs.docker.com/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)

---

## ✅ Documentation Checklist

Before starting, make sure you have read:

- [ ] [README.md](README.md) - Know what FoamAgent is
- [ ] [QUICKSTART.md](QUICKSTART.md) - Understand basic workflow
- [ ] Relevant troubleshooting section if issues arise

For deployment:
- [ ] [DEPLOYMENT.md](DEPLOYMENT.md) - Appropriate section for your environment
- [ ] [ARCHITECTURE.md](ARCHITECTURE.md) - System requirements and design

For development:
- [ ] [CONTRIBUTING.md](CONTRIBUTING.md) - Development guidelines
- [ ] [ARCHITECTURE.md](ARCHITECTURE.md) - Technical architecture
- [ ] [scripts/README.md](scripts/README.md) - Development tools

---

## 📝 Documentation Updates

This documentation is actively maintained. Last updated: March 2026

Found a documentation issue?
- Open an issue on GitHub
- Submit a pull request with corrections
- Suggest improvements

---

**Happy Computing! 🚀**
