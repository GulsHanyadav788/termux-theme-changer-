#!/bin/bash
# Termux Theme Changer Installation Script

echo "Installing Termux Theme Changer..."

# Check if running in Termux
if [ ! -d "/data/data/com.termux/files/home" ]; then
    echo "Error: This script must be run in Termux."
    exit 1
fi

# Update packages
echo "Updating packages..."
pkg update -y

# Install required packages
echo "Installing required packages..."
pkg install -y python git

# Install Python dependencies
echo "Installing Python dependencies..."
pip install pyyaml

# Clone the repository (if not already cloned)
if [ ! -d "termux-theme-changer" ]; then
    echo "Cloning repository..."
    git clone https://github.com/GulsHanyadav788/termux-theme-changer.git
fi

# Navigate to the directory
cd termux-theme-changer

# Make scripts executable
chmod +x main.py
chmod +x scripts/apply_theme.sh

echo "Installation completed!"
echo "To run the theme changer:"
echo "cd termux-theme-changer"
echo "python main.py"