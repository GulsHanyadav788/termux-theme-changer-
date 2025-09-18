#!/usr/bin/env python3
"""
Termex Theme Changer - A terminal theme management tool
Main application entry point
"""

import os
import sys
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("termex_theme_changer.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("termex_theme_changer")

# Import local modules
try:
    from theme_manager import ThemeManager
    from config_manager import ConfigManager
    from ui_manager import UIManager
except ImportError as e:
    logger.error(f"Failed to import required modules: {e}")
    print("Error: Required modules not found. Please install dependencies.")
    sys.exit(1)


class TermexThemeChanger:
    """Main application class for Termex Theme Changer"""
    
    def __init__(self):
        self.theme_manager = None
        self.config_manager = None
        self.ui_manager = None
        self.initialized = False
        
    def initialize(self) -> bool:
        """Initialize the application components"""
        try:
            # Define paths
            base_dir = Path(__file__).parent.absolute()
            themes_directory = base_dir / "themes"
            default_theme_path = themes_directory / "default"
            config_file = base_dir / "config" / "config.yaml"
            
            # Ensure directories exist
            themes_directory.mkdir(exist_ok=True, parents=True)
            config_file.parent.mkdir(exist_ok=True, parents=True)
            
            logger.info(f"Base directory: {base_dir}")
            logger.info(f"Themes directory: {themes_directory}")
            logger.info(f"Config file: {config_file}")
            
            # Initialize managers
            self.config_manager = ConfigManager(config_file)
            self.theme_manager = ThemeManager(self.config_manager, themes_directory, default_theme_path)
            self.ui_manager = UIManager()
            
            # Load configuration
            if not self.config_manager.load_config():
                logger.warning("Failed to load config, using defaults")
            
            # Verify theme directory exists and has themes
            if not self.theme_manager.verify_themes_directory():
                logger.warning(f"Themes directory not found at {themes_directory}")
                print("Warning: No themes directory found. Creating default structure...")
                self._create_default_theme_structure(themes_directory, default_theme_path)
                
            self.initialized = True
            logger.info("Application initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize application: {e}", exc_info=True)
            return False
    
    def _create_default_theme_structure(self, themes_dir: Path, default_theme_dir: Path) -> None:
        """Create default theme structure if it doesn't exist"""
        try:
            # Create default theme directory
            default_theme_dir.mkdir(exist_ok=True, parents=True)
            
            # Create a simple default theme
            default_theme = {
                "name": "default",
                "description": "Default terminal theme",
                "colors": {
                    "background": "#000000",
                    "foreground": "#FFFFFF",
                    "accent": "#3498DB"
                },
                "font": {
                    "family": "Monospace",
                    "size": 12
                }
            }
            
            # Write default theme file
            import json
            with open(default_theme_dir / "theme.json", "w") as f:
                json.dump(default_theme, f, indent=2)
                
            logger.info("Created default theme structure")
            
        except Exception as e:
            logger.error(f"Failed to create default theme structure: {e}")
    
    def display_available_themes(self) -> None:
        """Display all available themes"""
        try:
            themes = self.theme_manager.list_themes()
            if not themes:
                print("No themes available. Please add some themes to the themes directory.")
                return
                
            current_theme = self.theme_manager.get_current_theme_name()
            print("\nAvailable Themes:")
            for i, theme in enumerate(themes, 1):
                marker = " *" if theme == current_theme else ""
                print(f"{i}. {theme}{marker}")
            print()
            
        except Exception as e:
            logger.error(f"Error listing themes: {e}")
            print(f"Error: Failed to list themes. {e}")
    
    def apply_selected_theme(self) -> None:
        """Apply a theme selected by the user"""
        try:
            themes = self.theme_manager.list_themes()
            if not themes:
                print("No themes available to apply.")
                return
                
            self.display_available_themes()
            theme_name = self.ui_manager.get_theme_name()
            
            if not theme_name:
                print("No theme name provided.")
                return
                
            if theme_name in themes:
                success, message = self.theme_manager.apply_theme(theme_name)
                if success:
                    print(f"Theme '{theme_name}' applied successfully!")
                    print(message)
                else:
                    print(f"Failed to apply theme '{theme_name}': {message}")
            else:
                print(f"Theme '{theme_name}' not found. Please try again.")
                
        except Exception as e:
            logger.error(f"Error applying theme: {e}", exc_info=True)
            print(f"Error: Failed to apply theme. {e}")
    
    def revert_to_default_theme(self) -> None:
        """Revert to the default theme"""
        try:
            success, message = self.theme_manager.revert_to_default()
            if success:
                print("Reverted to default theme successfully!")
                print(message)
            else:
                print(f"Failed to revert to default theme: {message}")
        except Exception as e:
            logger.error(f"Error reverting to default theme: {e}")
            print(f"Error: Failed to revert to default theme. {e}")
    
    def show_current_theme(self) -> None:
        """Display the currently active theme"""
        try:
            current_theme = self.theme_manager.get_current_theme_name()
            if current_theme:
                print(f"\nCurrent theme: {current_theme}")
            else:
                print("\nNo theme is currently active.")
        except Exception as e:
            logger.error(f"Error getting current theme: {e}")
            print(f"Error: Failed to get current theme. {e}")
    
    def run(self) -> None:
        """Main application loop"""
        if not self.initialized:
            print("Application not properly initialized. Exiting.")
            return
            
        print("\n" + "="*50)
        print("      WELCOME TO TERMEX THEME CHANGER")
        print("="*50)
        
        while True:
            try:
                self.ui_manager.display_menu()
                choice = self.ui_manager.get_user_choice()
                
                if choice == '1':
                    self.display_available_themes()
                
                elif choice == '2':
                    self.apply_selected_theme()
                
                elif choice == '3':
                    self.revert_to_default_theme()
                
                elif choice == '4':
                    self.show_current_theme()
                
                elif choice == '5':
                    print("Exiting... Goodbye!")
                    break
                
                else:
                    print("Invalid choice, please try again.")
                    
            except KeyboardInterrupt:
                print("\n\nInterrupted by user. Exiting...")
                break
            except Exception as e:
                logger.error(f"Unexpected error in main loop: {e}", exc_info=True)
                print(f"An unexpected error occurred: {e}")
                print("Please try again.")


def main():
    """Main entry point for the application"""
    print("Initializing Termex Theme Changer...")
    
    app = TermexThemeChanger()
    
    if not app.initialize():
        print("Failed to initialize application. Exiting.")
        return 1
        
    try:
        app.run()
    except Exception as e:
        logger.error(f"Unexpected error in application: {e}", exc_info=True)
        print(f"Fatal error: {e}")
        return 1
        
    return 0


if __name__ == "__main__":
    sys.exit(main())