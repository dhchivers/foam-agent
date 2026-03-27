#!/bin/bash
# Project structure verification script

echo "FoamAgent Project Verification"
echo "==============================="
echo ""

# Function to check if file exists
check_file() {
    if [ -f "$1" ]; then
        echo "✓ $1"
    else
        echo "✗ $1 (MISSING)"
    fi
}

# Function to check if directory exists
check_dir() {
    if [ -d "$1" ]; then
        echo "✓ $1/"
    else
        echo "✗ $1/ (MISSING)"
    fi
}

echo "Documentation:"
check_file "README.md"
check_file "QUICKSTART.md"
check_file "DEPLOYMENT.md"
check_file "ARCHITECTURE.md"
check_file "TROUBLESHOOTING.md"
check_file "CONTRIBUTING.md"
check_file "PROJECT_SUMMARY.md"
check_file "DOCUMENTATION_INDEX.md"
check_file "LICENSE"

echo ""
echo "Build Configuration:"
check_file "Dockerfile"
check_file "CMakeLists.txt"
check_file "Makefile"
check_file ".dockerignore"
check_file ".gitignore"

echo ""
echo "Source Code:"
check_file "src/main.cpp"
check_file "src/mainwindow.h"
check_file "src/mainwindow.cpp"
check_file "src/casemanager.h"
check_file "src/casemanager.cpp"
check_file "src/meshwidget.h"
check_file "src/meshwidget.cpp"
check_file "src/solverwidget.h"
check_file "src/solverwidget.cpp"
check_file "src/visualizationwidget.h"
check_file "src/visualizationwidget.cpp"
check_file "src/processrunner.h"
check_file "src/processrunner.cpp"

echo ""
echo "UI Files:"
check_file "ui/mainwindow.ui"

echo ""
echo "Docker Configuration:"
check_file "docker/supervisord.conf"
check_file "docker/requirements.txt"
check_file "docker/.env"
check_file "docker/scripts/start.sh"

echo ""
echo "Scripts:"
check_file "start.sh"
check_file "scripts/build.sh"
check_file "scripts/run.sh"
check_file "scripts/dev.sh"
check_file "scripts/stop.sh"
check_file "scripts/logs.sh"
check_file "scripts/shell.sh"
check_file "scripts/README.md"

echo ""
echo "Examples:"
check_file "examples/templates/cavity/README.md"
check_file "examples/templates/cavity/blockMeshDict"

echo ""
echo "Work Directory:"
check_dir "work"
check_file "work/README.md"

echo ""
echo "Executable Permissions:"
if [ -x "start.sh" ]; then
    echo "✓ start.sh is executable"
else
    echo "✗ start.sh not executable (run: chmod +x start.sh)"
fi

for script in scripts/*.sh; do
    if [ -x "$script" ]; then
        echo "✓ $script is executable"
    else
        echo "✗ $script not executable (run: chmod +x $script)"
    fi
done

echo ""
echo "==============================="
echo "Verification complete!"
