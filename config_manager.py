"""
Configuration Manager for Termex Theme Changer
Handles configuration loading, saving, and management
"""

import os
import yaml
import json
from pathlib import Path
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger("termex_theme_changer.config_manager")


class ConfigManager:
    """Manages application configuration"""
    
    def __init__(self, config_file: Path):
        self.config_file = config_file
        self.config_data = {}
        self.default_config = {
            'current_theme': 'default',
            'auto_apply_on_start': False,
            'backup_before_apply': True,
            'terminal_emulator': 'auto',
            'theme_directory': str(Path.home() / '.termex' / 'themes')
        }
    
    def load_config(self) -> bool:
        """Load configuration from file"""
        try:
            if not self.config_file.exists():
                logger.warning(f"Config file {self.config_file} does not exist, using defaults")
                self.config_data = self.default_config.copy()
                return self.save_config()
            
            with open(self.config_file, 'r') as f:
                self.config_data = yaml.safe_load(f) or {}
                
            # Merge with defaults for any missing keys
            for key, value in self.default_config.items():
                if key not in self.config_data:
                    self.config_data[key] = value
                    
            logger.info(f"Loaded config from {self.config_file}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load config from {self.config_file}: {e}")
            self.config_data = self.default_config.copy()
            return False
    
    def save_config(self) -> bool:
        """Save configuration to file"""
        try:
            # Ensure config directory exists
            self.config_file.parent.mkdir(exist_ok=True, parents=True)
            
            with open(self.config_file, 'w') as f:
                yaml.dump(self.config_data, f, default_flow_style=False)
                
            logger.info(f"Saved config to {self.config_file}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save config to {self.config_file}: {e}")
            return False
    
    def get_config_value(self, key: str, default: Any = None) -> Any:
        """Get a configuration value"""
        return self.config_data.get(key, default)
    
    def set_config_value(self, key: str, value: Any) -> None:
        """Set a configuration value"""
        self.config_data[key] = value
    
    def get_all_config(self) -> Dict[str, Any]:
        """Get all configuration values"""
        return self.config_data.copy()