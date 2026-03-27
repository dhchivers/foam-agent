# Troubleshooting Guide

## Build Issues

### Docker Build Fails

**Problem**: Build fails with "Cannot connect to Docker daemon"

**Solution**:
```bash
# Check Docker is running
docker ps

# If not running, start Docker Desktop or daemon
# On macOS: Start Docker Desktop application
# On Linux: sudo systemctl start docker
```

**Problem**: Build fails with "No space left on device"

**Solution**:
```bash
# Clean up Docker
docker system prune -a

# Remove unused images
docker image prune -a
```

**Problem**: OpenFOAM installation fails

**Solution**:
- Check internet connection
- Retry build: `./scripts/build.sh`
- If persistent, check OpenFOAM repository status at https://dl.openfoam.org

### Qt6 Compilation Errors

**Problem**: "Could not find Qt6" during build

**Solution**: The Dockerfile should handle this automatically. If it fails:
```bash
# Rebuild with no cache
docker build --no-cache -t foamagent:latest -f Dockerfile .
```

## Runtime Issues

### Cannot Access Web Interface

**Problem**: Browser shows "Unable to connect" at localhost:6080

**Solution**:
```bash
# Check container is running
docker ps | grep foamagent

# Check port mappings
docker port foamagent

# View container logs
docker logs foamagent

# Restart container
docker restart foamagent
```

**Problem**: Blank screen in browser

**Solution**:
- Wait 10-15 seconds for services to fully start
- Check supervisor status:
  ```bash
  docker exec -it foamagent supervisorctl status
  ```
- Restart VNC:
  ```bash
  docker exec -it foamagent supervisorctl restart vncserver
  ```

### VNC Connection Issues

**Problem**: "Connection failed" in noVNC

**Solution**:
```bash
# Check all services are running
docker exec -it foamagent supervisorctl status

# Expected output:
# novnc      RUNNING
# vncserver  RUNNING
# xvfb       RUNNING
# foamagent  RUNNING

# Restart all services if needed
docker exec -it foamagent supervisorctl restart all
```

**Problem**: Black screen with cursor only

**Solution**:
- This means VNC is working but the GUI hasn't started
- Check FoamAgent process:
  ```bash
  docker exec -it foamagent supervisorctl status foamagent
  ```
- View FoamAgent logs:
  ```bash
  docker exec -it foamagent tail -f /var/log/supervisor/foamagent.log
  ```

## Application Issues

### Cannot Create or Open Cases

**Problem**: "Failed to create case" error

**Solution**:
- Check permissions on `/work` directory
- Verify directory exists inside container:
  ```bash
  docker exec -it foamagent ls -la /work
  ```
- Ensure host `work` directory is accessible:
  ```bash
  ls -la /Users/chivers/FoamAgent/work
  ```

**Problem**: "Invalid OpenFOAM case structure"

**Solution**:
- Ensure case has required directories: `0`, `constant`, `system`
- Check for `system/controlDict` file
- Validate case structure manually:
  ```bash
  docker exec -it foamagent bash
  cd /work/myCase
  ls -R
  ```

### Mesh Generation Fails

**Problem**: blockMesh fails with "Cannot find blockMeshDict"

**Solution**:
- Create `blockMeshDict` in `constant/polyMesh/` directory
- Use example template from `examples/templates/cavity/`
- Check file permissions and location

**Problem**: "Bad mesh" or quality warnings

**Solution**:
- Run mesh quality check: Click "Check Quality" button
- Review mesh parameters (cell count, aspect ratio)
- Simplify geometry or refine mesh
- Check blockMeshDict for errors

### Solver Issues

**Problem**: Solver fails to start

**Solution**:
```bash
# Check OpenFOAM environment
docker exec -it foamagent bash
source /opt/openfoam2312/etc/bashrc
which icoFoam

# Test solver manually
cd /work/myCase
icoFoam
```

**Problem**: "Floating point exception" during solve

**Solution**:
- Check initial conditions in `0/` directory
- Verify boundary conditions are physically reasonable
- Reduce time step in `system/controlDict`
- Check mesh quality

**Problem**: Solver runs but produces no output

**Solution**:
- Check `writeControl` and `writeInterval` in `controlDict`
- Verify disk space: `df -h`
- Check solver output logs in application

### Visualization Issues

**Problem**: ParaView won't launch

**Solution**:
```bash
# Test ParaView manually
docker exec -it foamagent bash
DISPLAY=:1 paraview

# Check X11 display
echo $DISPLAY
```

**Problem**: "No data to display"

**Solution**:
- Run solver first to generate results
- Check that time directories exist
- Create `.foam` file: `touch case.foam`
- Open `.foam` file in ParaView

## Performance Issues

### Slow GUI Response

**Solution**:
- Reduce VNC resolution:
  ```bash
  VNC_RESOLUTION=1280x720 ./scripts/run.sh
  ```
- Increase container resources in Docker settings
- Close unnecessary applications

### High CPU Usage

**Solution**:
- This is normal during solver execution
- Monitor with: `docker stats foamagent`
- Reduce mesh density for faster solving
- Use steady-state solvers when possible

## Data Persistence

### Lost Data After Container Restart

**Problem**: Cases disappear after stopping container

**Solution**:
- Always save cases in `/work` directory
- Verify volume mount: `docker inspect foamagent | grep Mounts -A 10`
- Check host directory: `ls /Users/chivers/FoamAgent/work`

**Problem**: Cannot modify files in work directory

**Solution**:
```bash
# Check permissions
ls -la /Users/chivers/FoamAgent/work

# Fix permissions if needed (on host)
chmod -R 755 /Users/chivers/FoamAgent/work
```

## Docker Issues

### Container Won't Start

**Solution**:
```bash
# View error logs
docker logs foamagent

# Remove and recreate
docker rm foamagent
./scripts/run.sh
```

### Port Already in Use

**Problem**: "port is already allocated" error

**Solution**:
```bash
# Find what's using the port
lsof -i :6080
lsof -i :5901

# Stop the conflicting service or change ports
docker run ... -p 6081:6080 -p 5902:5901 ...
```

## Development Issues

### Code Changes Not Reflected

**Problem**: Built application doesn't show changes

**Solution**:
```bash
# Use development mode
./scripts/dev.sh

# Rebuild inside container
docker exec -it foamagent-dev bash
cd /app/build
cmake ..
make
supervisorctl restart foamagent
```

## Getting More Help

### Collect Diagnostic Information

When reporting issues, include:

```bash
# System info
docker --version
docker info

# Container logs
docker logs foamagent > foamagent-logs.txt

# Supervisor status
docker exec -it foamagent supervisorctl status

# Service logs
docker exec -it foamagent cat /var/log/supervisor/foamagent.log
docker exec -it foamagent cat /var/log/supervisor/vnc.log
```

### Common Log Locations

- Supervisor: `/var/log/supervisor/supervisord.log`
- VNC: `/var/log/supervisor/vnc.log`
- noVNC: `/var/log/supervisor/novnc.log`
- FoamAgent: `/var/log/supervisor/foamagent.log`

### Reset Everything

Nuclear option - complete reset:

```bash
# Stop and remove container
docker stop foamagent
docker rm foamagent

# Remove image
docker rmi foamagent:latest

# Rebuild from scratch
./scripts/build.sh
./scripts/run.sh
```

## Still Having Issues?

- Check existing GitHub issues
- Open a new issue with diagnostic information
- Include logs and steps to reproduce
- Specify your environment (OS, Docker version, etc.)
