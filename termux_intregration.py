"""
Termux Integration for Termux Theme Changer
Handles Termux-specific functionality
"""

import os
import subprocess
from pathlib import Path
from typing import Tuple
import logging

logger = logging.getLogger("termux_theme_changer.termux_integration")


class TermuxIntegration:
    """Handles Termux-specific operations"""
    
    def __init__(self):
        self.termux_home = Path("/data/data/com.termux/files/home")
        self.termux_config_dir = self.termux_home / ".termux"
    
    def reload_termux_session(self) -> Tuple[bool, str]:
        """Reload Termux session to apply theme changes"""
        try:
            # Create .termux directory if it doesn't exist
            self.termux_config_dir.mkdir(exist_ok=True)
            
            # Run termux-reload-settings command
            result = subprocess.run(
                ["termux-reload-settings"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return True, "Termux settings reloaded successfully."
            else:
                return False, f"Failed to reload Termux settings: {result.stderr}"
                
        except subprocess.TimeoutExpired:
            return False, "Timeout while reloading Termux settings."
        except Exception as e:
            logger.error(f"Error reloading Termux session: {e}")
            return False, f"Error reloading Termux session: {e}"
    
    def check_termux_installation(self) -> Tuple[bool, str]:
        """Check if Termux is properly installed"""
        try:
            # Check if Termux home directory exists
            if not self.termux_home.exists():
                return False, "Termux home directory not found. Please install Termux."
            
            # Check if termux-reload-settings command is available
            result = subprocess.run(
                ["which", "termux-reload-settings"],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                return False, "termux-reload-settings command not found. Please install Termux:API package."
            
            return True, "Termux installation verified."
            
        except Exception as e:
            logger.error(f"Error checking Termux installation: {e}")
            return False, f"Error checking Termux installation: {e}"
    
    def install_termux_api(self) -> Tuple[bool, str]:
        """Install Termux:API package if not installed"""
        try:
            result = subprocess.run(
                ["pkg", "install", "-y", "termux-api"],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                return True, "Termux:API installed successfully."
            else:
                return False, f"Failed to install Termux:API: {result.stderr}"
                
        except subprocess.TimeoutExpired:
            return False, "Timeout while installing Termux:API."
        except Exception as e:
            logger.error(f"Error installing Termux:API: {e}")
            return False, f"Error installing Termux:API: {e}"