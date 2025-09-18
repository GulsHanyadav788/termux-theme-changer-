"""
Theme Manager for Termex Theme Changer
Handles theme discovery, application, and management
"""

import os
import json
import shutil
import logging
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional

logger = logging.getLogger("termex_theme_changer.theme_manager")


class ThemeManager:
    """Manages terminal themes"""
    
    def __init__(self, config_manager, themes_directory: Path, default_theme_path: Path):
        self.config_manager = config_manager
        self.themes_directory = themes_directory
        self.default_theme_path = default_theme_path
        self.current_theme = None
        
    def verify_themes_directory(self) -> bool:
        """Verify that the themes directory exists and contains themes"""
        if not self.themes_directory.exists():
            return False
            
        # Check if there are any theme directories
        theme_dirs = [d for d in self.themes_directory.iterdir() 
                     if d.is_dir() and not d.name.startswith('.')]
        return len(theme_dirs) > 0
    
    def list_themes(self) -> List[str]:
        """List all available themes"""
        themes = []
        if not self.themes_directory.exists():
            return themes
            
        for theme_dir in self.themes_directory.iterdir():
            if theme_dir.is_dir() and not theme_dir.name.startswith('.'):
                themes.append(theme_dir.name)
                
        return sorted(themes)
    
    def get_theme_info(self, theme_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific theme"""
        theme_path = self.themes_directory / theme_name
        theme_file = theme_path / "theme.json"
        
        if not theme_file.exists():
            return None
            
        try:
            with open(theme_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Failed to read theme file {theme_file}: {e}")
            return None
    
    def apply_theme(self, theme_name: str) -> Tuple[bool, str]:
        """Apply a theme to the terminal"""
        try:
            theme_info = self.get_theme_info(theme_name)
            if not theme_info:
                return False, f"Theme '{theme_name}' not found or invalid"
            
            # Here you would implement the actual theme application logic
            # This will vary depending on your terminal emulator
            
            # Example: For iTerm2, you might use AppleScript
            # Example: For Windows Terminal, you might modify settings.json
            
            # For demonstration, we'll just set the current theme
            self.current_theme = theme_name
            
            # Save to config
            self.config_manager.set_config_value('current_theme', theme_name)
            self.config_manager.save_config()
            
            logger.info(f"Applied theme: {theme_name}")
            return True, f"Theme '{theme_name}' applied successfully"
            
        except Exception as e:
            logger.error(f"Failed to apply theme '{theme_name}': {e}")
            return False, f"Failed to apply theme: {e}"
    
    def revert_to_default(self) -> Tuple[bool, str]:
        """Revert to the default theme"""
        return self.apply_theme("default")
    
    def get_current_theme_name(self) -> Optional[str]:
        """Get the name of the currently applied theme"""
        if self.current_theme:
            return self.current_theme
            
        # Try to get from config
        return self.config_manager.get_config_value('current_theme')
    
    def create_theme(self, theme_name: str, theme_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Create a new theme"""
        try:
            theme_path = self.themes_directory / theme_name
            theme_path.mkdir(exist_ok=True)
            
            theme_file = theme_path / "theme.json"
            with open(theme_file, 'w') as f:
                json.dump(theme_data, f, indent=2)
                
            logger.info(f"Created new theme: {theme_name}")
            return True, f"Theme '{theme_name}' created successfully"
            
        except Exception as e:
            logger.error(f"Failed to create theme '{theme_name}': {e}")
            return False, f"Failed to create theme: {e}"
    
    def delete_theme(self, theme_name: str) -> Tuple[bool, str]:
        """Delete a theme"""
        try:
            if theme_name == "default":
                return False, "Cannot delete the default theme"
                
            theme_path = self.themes_directory / theme_name
            if not theme_path.exists():
                return False, f"Theme '{theme_name}' does not exist"
                
            shutil.rmtree(theme_path)
            logger.info(f"Deleted theme: {theme_name}")
            return True, f"Theme '{theme_name}' deleted successfully"
            
        except Exception as e:
            logger.error(f"Failed to delete theme '{theme_name}': {e}")
            return False, f"Failed to delete theme: {e}"