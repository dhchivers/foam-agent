# Scripts Directory

This directory contains shell scripts for building, running, and managing the FoamAgent Docker container.

## Available Scripts

### build.sh
Builds the FoamAgent Docker image from scratch.

```bash
./scripts/build.sh
```

**What it does:**
- Builds Docker image tagged as `foamagent:latest`
- Installs Ubuntu, Qt6, OpenFOAM, ParaView, VNC stack
- Compiles the Qt6 application
- Takes 10-20 minutes on first run

**When to use:**
- Initial setup
- After pulling code changes
- When Dockerfile is modified
- To rebuild with latest dependencies

---

### run.sh
Starts the FoamAgent container in normal mode.

```bash
./scripts/run.sh
```

**What it does:**
- Stops any existing container
- Starts new container with volume mounts
- Exposes ports 5901 (VNC) and 6080 (web)
- Maps `work/` directory for persistent storage

**Configuration:**
```bash
# Custom resolution
VNC_RESOLUTION=1280x720 ./scripts/run.sh

# Custom password
VNC_PASSWORD=mysecret ./scripts/run.sh

# Custom container name
CONTAINER_NAME=myfoam ./scripts/run.sh
```

---

### dev.sh
Starts the container in development mode with live code mounting.

```bash
./scripts/dev.sh
```

**What it does:**
- Same as run.sh but mounts source code directories
- Changes to `src/` and `ui/` are immediately available
- Requires rebuild inside container to take effect
- Container named `foamagent-dev`

**Workflow:**
1. Start dev container: `./scripts/dev.sh`
2. Edit code on host
3. Rebuild in container: `docker exec -it foamagent-dev bash -c 'cd /app/build && cmake .. && make'`
4. Restart app: `docker exec -it foamagent-dev supervisorctl restart foamagent`

---

### stop.sh
Stops the running FoamAgent container.

```bash
./scripts/stop.sh
```

**What it does:**
- Gracefully stops the container
- Containers can be restarted with `docker start foamagent`

---

### logs.sh
View real-time logs from the container.

```bash
./scripts/logs.sh
```

**What it does:**
- Streams container logs to terminal
- Shows all service output (VNC, noVNC, FoamAgent)
- Press Ctrl+C to exit

**Useful for:**
- Debugging startup issues
- Monitoring application behavior
- Watching solver progress

---

### shell.sh
Opens a bash shell inside the running container.

```bash
./scripts/shell.sh
```

**What it does:**
- Opens interactive shell in container
- OpenFOAM environment pre-loaded
- Full access to container filesystem

**Common uses:**
```bash
# Check OpenFOAM installation
which icoFoam

# Navigate to case
cd /work/myCase

# Run OpenFOAM commands directly
blockMesh
icoFoam

# Check running processes
ps aux | grep foam

# View supervisor status
supervisorctl status
```

---

## Quick Reference

```bash
# Initial setup
./scripts/build.sh          # Build (once)
./scripts/run.sh            # Run

# Daily use
./scripts/stop.sh           # Stop when done
./scripts/run.sh            # Restart later

# Debugging
./scripts/logs.sh           # View logs
./scripts/shell.sh          # Access shell

# Development
./scripts/dev.sh            # Dev mode
```

## Make Command Equivalents

If you prefer Make:

```bash
make build    # → ./scripts/build.sh
make run      # → ./scripts/run.sh
make dev      # → ./scripts/dev.sh
make stop     # → ./scripts/stop.sh
make logs     # → ./scripts/logs.sh
make shell    # → ./scripts/shell.sh
```

## Environment Variables

All scripts support these environment variables:

- `VNC_RESOLUTION`: Set display resolution (default: 1920x1080)
- `VNC_PASSWORD`: Set VNC password (default: foamagent)
- `CONTAINER_NAME`: Set container name (default: foamagent)

Example:
```bash
VNC_RESOLUTION=1280x720 VNC_PASSWORD=secret ./scripts/run.sh
```

## Permissions

All scripts should be executable. If not:

```bash
chmod +x scripts/*.sh
```

## Troubleshooting

**Script not found or permission denied:**
```bash
cd /Users/chivers/FoamAgent
chmod +x scripts/*.sh
```

**Docker command not found:**
- Ensure Docker is installed and running
- Check Docker Desktop is started (macOS)

**Container already exists:**
- Use `./scripts/stop.sh` first
- Or manually: `docker rm -f foamagent`

**Port already in use:**
- Stop other services using ports 5901 or 6080
- Or change ports in run.sh

For more troubleshooting, see TROUBLESHOOTING.md in the project root.
