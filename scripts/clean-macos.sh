#!/bin/bash
# Clean macOS metadata files (._* files and .DS_Store)
# These files can interfere with Docker builds and version control

set -e

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "Cleaning macOS metadata files..."
echo "Project directory: $PROJECT_DIR"
echo ""

# Find and remove ._* files (AppleDouble format / resource forks)
echo "Removing ._* files..."
find "$PROJECT_DIR" -type f -name "._*" -print -delete

# Find and remove .DS_Store files
echo "Removing .DS_Store files..."
find "$PROJECT_DIR" -type f -name ".DS_Store" -print -delete

# Count remaining files (should be 0)
REMAINING_APPLE=$(find "$PROJECT_DIR" -type f -name "._*" | wc -l)
REMAINING_DS=$(find "$PROJECT_DIR" -type f -name ".DS_Store" | wc -l)

echo ""
echo "Cleanup complete!"
echo "Remaining ._* files: $REMAINING_APPLE"
echo "Remaining .DS_Store files: $REMAINING_DS"

if [ "$REMAINING_APPLE" -eq 0 ] && [ "$REMAINING_DS" -eq 0 ]; then
    echo "✓ All macOS metadata files removed successfully"
else
    echo "⚠ Warning: Some files may still remain"
fi
