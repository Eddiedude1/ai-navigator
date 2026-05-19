#!/bin/bash

# Tricentis Development Environment Setup Script
# Creates a virtual environment using uv and installs required dependencies

set -e  # Exit on any error

NAME=navigator
VENV_DIR="py-${NAME}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_status "Starting Tricentis development environment setup..."

# Check for uv
if ! command -v uv >/dev/null 2>&1; then
    print_error "uv is not installed."
    print_error "Install it with: curl -LsSf https://astral.sh/uv/install.sh | sh"
    print_error "Or visit: https://docs.astral.sh/uv/getting-started/installation/"
    exit 1
fi

print_status "Found uv: $(uv --version)"

# Check for git
if ! command -v git >/dev/null 2>&1; then
    print_warning "Git is not installed. You may need it for version control."
fi

# Remove existing virtual environment if it exists
if [ -d "$VENV_DIR" ]; then
    print_status "Removing existing virtual environment..."
    rm -rf "$VENV_DIR"
fi

# Create virtual environment with Python 3.13
print_status "Creating virtual environment: $VENV_DIR (Python 3.13)"
uv venv "$VENV_DIR" --python 3.13

# Activate virtual environment
print_status "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Install dependencies from requirements.txt
print_status "Installing project dependencies..."
uv pip install -r requirements.txt

# Install Playwright browsers
print_status "Installing Playwright browser binaries..."
python -m playwright install chromium

print_status "Setup completed successfully!"
print_status ""
print_status "To activate the environment in the future, run:"
print_status "  . ${VENV_DIR}/bin/activate"
print_status ""
print_status "To deactivate the environment, run:"
print_status "  deactivate"
