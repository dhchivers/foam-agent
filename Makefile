# Makefile for FoamAgent
# Convenience wrapper around Docker commands

.PHONY: help build run dev stop logs shell clean rebuild

# Default target
help:
	@echo "FoamAgent - Make targets:"
	@echo ""
	@echo "  make build    - Build the Docker container"
	@echo "  make run      - Run the application"
	@echo "  make dev      - Run in development mode"
	@echo "  make stop     - Stop the container"
	@echo "  make logs     - View container logs"
	@echo "  make shell    - Access container shell"
	@echo "  make clean    - Stop and remove container"
	@echo "  make rebuild  - Clean, rebuild, and run"
	@echo ""
	@echo "After running, access at: http://localhost:6080"

# Build the Docker container
build:
	@./scripts/build.sh

# Run the application
run:
	@./scripts/run.sh

# Run in development mode
dev:
	@./scripts/dev.sh

# Stop the container
stop:
	@./scripts/stop.sh

# View logs
logs:
	@./scripts/logs.sh

# Access shell
shell:
	@./scripts/shell.sh

# Clean up
clean:
	@echo "Stopping and removing container..."
	@docker stop foamagent 2>/dev/null || true
	@docker rm foamagent 2>/dev/null || true
	@echo "✓ Cleanup complete"

# Full rebuild
rebuild: clean build run
	@echo ""
	@echo "✓ Rebuild complete!"
	@echo "Access at: http://localhost:6080"
