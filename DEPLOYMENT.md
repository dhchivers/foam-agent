# FoamAgent Deployment Guide

## Overview

This guide covers deploying FoamAgent in various environments, from local development to production servers.

## Table of Contents

1. [Local Development](#local-development)
2. [Production Server](#production-server)
3. [Cloud Deployment](#cloud-deployment)
4. [Scaling and Load Balancing](#scaling)
5. [Security Hardening](#security)
6. [Backup and Recovery](#backup)
7. [Monitoring](#monitoring)

---

## Local Development

### Quick Start (macOS/Linux)

```bash
# Clone or navigate to project
cd /Users/chivers/FoamAgent

# One-command setup and launch
./start.sh

# Or manual steps:
./scripts/build.sh   # First time only
./scripts/run.sh     # Start container
```

### Windows (PowerShell)

```powershell
# Ensure Docker Desktop is running
docker --version

# Build image
docker build -t foamagent:latest -f Dockerfile .

# Run container
docker run -d `
  --name foamagent `
  -p 5901:5901 `
  -p 6080:6080 `
  -v ${PWD}/work:/work `
  --shm-size=2g `
  foamagent:latest

# Access at http://localhost:6080
```

### Development Mode

For active development with live code updates:

```bash
# Start in dev mode
./scripts/dev.sh

# Edit code in src/ or ui/

# Rebuild inside container
docker exec -it foamagent-dev bash
cd /app/build
cmake ..
make -j$(nproc)
supervisorctl restart foamagent
exit

# Or use one-liner:
docker exec -it foamagent-dev bash -c \
  'cd /app/build && cmake .. && make && supervisorctl restart foamagent'
```

---

## Production Server

### Prerequisites

- Ubuntu Server 20.04+ or RHEL 8+
- Docker Engine 20.10+
- 8GB+ RAM
- 50GB+ disk space
- Open ports: 6080, 5901 (optional)

### Installation

```bash
# Install Docker (Ubuntu)
sudo apt-get update
sudo apt-get install -y docker.io docker-compose
sudo systemctl enable docker
sudo systemctl start docker

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Clone repository
git clone <your-repo-url> /opt/foamagent
cd /opt/foamagent

# Build image
./scripts/build.sh

# Create systemd service
sudo cp deployment/foamagent.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable foamagent
sudo systemctl start foamagent
```

### Systemd Service

Create `/etc/systemd/system/foamagent.service`:

```ini
[Unit]
Description=FoamAgent - OpenFOAM GUI Container
After=docker.service
Requires=docker.service

[Service]
Type=forking
RemainAfterExit=yes
WorkingDirectory=/opt/foamagent
ExecStart=/opt/foamagent/scripts/run.sh
ExecStop=/opt/foamagent/scripts/stop.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### NGINX Reverse Proxy

```nginx
server {
    listen 80;
    server_name foamagent.example.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name foamagent.example.com;
    
    ssl_certificate /etc/ssl/certs/foamagent.crt;
    ssl_certificate_key /etc/ssl/private/foamagent.key;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    location / {
        proxy_pass http://localhost:6080/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_connect_timeout 7d;
        proxy_send_timeout 7d;
        proxy_read_timeout 7d;
    }
}
```

Apply configuration:

```bash
sudo ln -s /etc/nginx/sites-available/foamagent /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## Cloud Deployment

### AWS EC2

```bash
# Launch EC2 instance
# - AMI: Ubuntu Server 22.04 LTS
# - Instance type: t3.xlarge (or larger)
# - Storage: 50GB+ EBS
# - Security Group: Allow 22 (SSH), 80, 443

# SSH into instance
ssh -i key.pem ubuntu@<instance-ip>

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Deploy FoamAgent
git clone <repo-url>
cd FoamAgent
./scripts/build.sh
./scripts/run.sh

# Setup reverse proxy (see NGINX section above)
```

### Google Cloud Platform (GCP)

```bash
# Create VM instance
gcloud compute instances create foamagent \
  --machine-type=n1-standard-4 \
  --boot-disk-size=50GB \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --tags=http-server,https-server

# SSH and deploy (same as AWS)
```

### Azure

```bash
# Create VM
az vm create \
  --resource-group foamagent-rg \
  --name foamagent-vm \
  --image UbuntuLTS \
  --size Standard_D4s_v3 \
  --admin-username azureuser \
  --generate-ssh-keys

# Open ports
az vm open-port --port 80 --resource-group foamagent-rg --name foamagent-vm
az vm open-port --port 443 --resource-group foamagent-rg --name foamagent-vm

# SSH and deploy
```

### Docker Compose (Recommended for Production)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  foamagent:
    image: foamagent:latest
    container_name: foamagent
    restart: unless-stopped
    ports:
      - "127.0.0.1:5901:5901"
      - "127.0.0.1:6080:6080"
    volumes:
      - ./work:/work
      - foamagent-logs:/var/log/supervisor
    environment:
      - VNC_RESOLUTION=1920x1080
      - VNC_PASSWORD=${VNC_PASSWORD:-foamagent}
    shm_size: 2gb
    
  nginx:
    image: nginx:alpine
    container_name: foamagent-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    depends_on:
      - foamagent

volumes:
  foamagent-logs:
```

Deploy:

```bash
docker-compose up -d
docker-compose logs -f
```

---

## Scaling

### Multiple Instances

Run multiple containers on different ports:

```bash
# Instance 1
docker run -d --name foamagent-1 -p 6081:6080 -p 5902:5901 \
  -v ./work1:/work foamagent:latest

# Instance 2
docker run -d --name foamagent-2 -p 6082:6080 -p 5903:5901 \
  -v ./work2:/work foamagent:latest

# Instance 3
docker run -d --name foamagent-3 -p 6083:6080 -p 5904:5901 \  -v ./work3:/work foamagent:latest
```

### Load Balancing (NGINX)

```nginx
upstream foamagent_backend {
    least_conn;
    server localhost:6081;
    server localhost:6082;
    server localhost:6083;
}

server {
    listen 80;
    
    location / {
        proxy_pass http://foamagent_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Sticky sessions (important for VNC)
        ip_hash;
    }
}
```

---

## Security

### Authentication Layer

Add authentication using nginx-auth:

```bash
# Install htpasswd
sudo apt-get install apache2-utils

# Create password file
sudo htpasswd -c /etc/nginx/.htpasswd admin

# Add to nginx config
location / {
    auth_basic "FoamAgent Access";
    auth_basic_user_file /etc/nginx/.htpasswd;
    proxy_pass http://localhost:6080/;
}
```

### Firewall Configuration

```bash
# UFW (Ubuntu)
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable

# Firewalld (RHEL/CentOS)
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

### SSL/TLS Certificates

```bash
# Using Let's Encrypt
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d foamagent.example.com
sudo certbot renew --dry-run
```

---

## Backup

### Automated Backup Script

Create `/opt/foamagent/backup.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/backups/foamagent"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup work directory
tar -czf "$BACKUP_DIR/work_$DATE.tar.gz" /opt/foamagent/work

# Backup Docker image
docker save foamagent:latest | gzip > "$BACKUP_DIR/image_$DATE.tar.gz"

# Keep only last 7 days
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
```

### Cron Job

```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * /opt/foamagent/backup.sh >> /var/log/foamagent-backup.log 2>&1
```

---

## Monitoring

### Health Check Script

Create `/opt/foamagent/healthcheck.sh`:

```bash
#!/bin/bash

# Check container is running
if [ ! "$(docker ps -q -f name=foamagent)" ]; then
    echo "ERROR: Container not running"
    # Restart
    /opt/foamagent/scripts/run.sh
    exit 1
fi

# Check web interface responds
if ! curl -f -s -o /dev/null http://localhost:6080; then
    echo "ERROR: Web interface not responding"
    docker restart foamagent
    exit 1
fi

echo "OK: All checks passed"
exit 0
```

### Prometheus Metrics (Optional)

Expose container metrics:

```bash
# Install cAdvisor
docker run -d \
  --name=cadvisor \
  --restart=always \
  -v /:/rootfs:ro \
  -v /var/run:/var/run:ro \
  -v /sys:/sys:ro \
  -v /var/lib/docker/:/var/lib/docker:ro \
  -p 8080:8080 \
  gcr.io/cadvisor/cadvisor:latest
```

### Log Aggregation

Centralized logging with rsyslog:

```bash
# Forward logs to remote server
logger -t foamagent -p local0.info "$(docker logs foamagent)"
```

---

## Troubleshooting Deployment

### Container won't start

```bash
# Check Docker logs
docker logs foamagent

# Check system resources
free -h
df -h

# Check port conflicts
netstat -tulpn | grep -E '6080|5901'
```

### Performance issues

```bash
# Increase container resources
docker update --memory="8g" --cpus="4" foamagent

# Monitor resource usage
docker stats foamagent
```

### Network connectivity

```bash
# Test from inside container
docker exec -it foamagent curl -I localhost:6080

# Test from host
curl -I localhost:6080

# Check firewall
sudo iptables -L -n | grep -E '6080|5901'
```

---

## Maintenance

### Regular Updates

```bash
# Pull latest code
cd /opt/foamagent
git pull

# Rebuild image
./scripts/build.sh

# Restart (with backup)
./backup.sh
docker stop foamagent
docker rm foamagent
./scripts/run.sh
```

### Log Rotation

Configure in `/etc/logrotate.d/foamagent`:

```
/var/log/foamagent/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0644 root root
}
```

---

## Support

For deployment issues:
- Review logs: `./scripts/logs.sh`
- Check health: `/opt/foamagent/healthcheck.sh`
- See troubleshooting: TROUBLESHOOTING.md

For production support:
- Monitor system resources
- Review NGINX logs: `/var/log/nginx/`
- Check Docker logs: `docker logs foamagent`
