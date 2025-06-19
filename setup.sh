#!/bin/bash

# Tricentis Development Environment Setup Script
# This script creates a Python virtual environment and installs required dependencies

set -e  # Exit on any error

NAME=tricentis
VENV_DIR="py-${NAME}"
MIN_PYTHON_VERSION="3.8"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to compare version numbers
version_compare() {
    printf '%s\n%s\n' "$2" "$1" | sort -V -C
}

# Function to get Python version
get_python_version() {
    $1 -c "import sys; print('.'.join(map(str, sys.version_info[:2])))" 2>/dev/null
}

# Function to find suitable Python executable
find_python() {
    local python_candidates=("python3" "python" "python3.8" "python3.9" "python3.10" "python3.11")
    
    for candidate in "${python_candidates[@]}"; do
        if command_exists "$candidate"; then
            local version=$(get_python_version "$candidate")
            if [ $? -eq 0 ] && version_compare "$version" "$MIN_PYTHON_VERSION"; then
                echo "$candidate"
                return 0
            fi
        fi
    done
    
    return 1
}

print_status "Starting Tricentis development environment setup..."

# Check for required system dependencies
print_status "Checking system requirements..."

# Find Python executable
print_status "Looking for suitable Python installation..."
PYTHON_EXEC=$(find_python)

if [ $? -ne 0 ]; then
    print_error "No suitable Python installation found!"
    print_error "Please install Python ${MIN_PYTHON_VERSION} or higher."
    print_error "Visit https://www.python.org/downloads/ for installation instructions."
    exit 1
fi

PYTHON_VERSION=$(get_python_version "$PYTHON_EXEC")
print_status "Found Python ${PYTHON_VERSION} at: $(which $PYTHON_EXEC)"

# Check if pip is available
if ! $PYTHON_EXEC -m pip --version >/dev/null 2>&1; then
    print_error "pip is not available for the selected Python installation."
    print_error "Please install pip or use a Python installation that includes pip."
    exit 1
fi

# Check if git is available (often needed for development)
if ! command_exists git; then
    print_warning "Git is not installed. You may need it for version control."
fi

# Remove existing virtual environment if it exists
if [ -d "$VENV_DIR" ]; then
    print_status "Removing existing virtual environment..."
    rm -rf "$VENV_DIR"
fi

# Create virtual environment
print_status "Creating Python virtual environment: $VENV_DIR"
$PYTHON_EXEC -m venv "$VENV_DIR"

# Activate virtual environment
print_status "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Verify we're in the virtual environment
if [ "$VIRTUAL_ENV" != "$(pwd)/$VENV_DIR" ]; then
    print_error "Failed to activate virtual environment"
    exit 1
fi

print_status "Virtual environment activated: $VIRTUAL_ENV"

# Upgrade pip and essential tools
print_status "Upgrading pip and essential tools..."
python -m pip install --upgrade pip
python -m pip install --upgrade wheel
python -m pip install --upgrade setuptools

# Install project dependencies
print_status "Installing project dependencies..."
python -m pip install --no-cache-dir selenium
python -m pip install --no-cache-dir anthropic
python -m pip install --no-cache-dir python-dotenv
python -m pip install --no-cache-dir toml
python -m pip install --no-cache-dir playwright==1.10.0
python -m pip install --no-cache-dir pyee==8.2.2
python -m pip install --no-cache-dir undetected-playwright==0.3.0

# Install Playwright browsers
print_status "Installing Playwright browser binaries..."
python -m playwright install chromium

print_status "Setup completed successfully!"
print_status ""
print_status "To activate the environment in the future, run:"
print_status "$ . ${VENV_DIR}/bin/activate"
print_status ""
print_status "To deactivate the environment, run:"
print_status "  deactivate"
print_status ""
print_status "Happy coding! 🚀"
