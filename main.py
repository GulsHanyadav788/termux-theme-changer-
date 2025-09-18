#!/usr/bin/env python3
"""
Termux Theme Changer - Enhance your Termux terminal appearance
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
        logging.FileHandler("/data/data/com.termux/files/home/termux_theme_changer.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("termux_theme_changer")

# Import local modules
try:
    from theme_manager import ThemeManager
    from config_manager import ConfigManager
    from ui_manager import UIManager
    from termux_integration import TermuxIntegration
except ImportError as e:
    logger.error(f"Failed to import required modules: {e}")
    print("Error: Required modules not found. Please install dependencies.")
    sys.exit(1)


class TermuxThemeChanger:
    """Main application class for Termux Theme Changer"""
    
    def __init__(self):
        self.theme_manager = None
        self.config_manager = None
        self.ui_manager = None
        self.termux_integration = None
        self.initialized = False
        
    def initialize(self) -> bool:
        """Initialize the application components"""
        try:
            # Check if we're running in Termux
            if not self._is_termux_environment():
                print("Error: This tool is designed to run in Termux on Android.")
                print("Please run this script inside Termux.")
                return False
            
            # Define paths
            base_dir = Path(__file__).parent.absolute()
            themes_directory = base_dir / "themes"
            config_file = base_dir / "config" / "config.yaml"
            
            # Ensure directories exist
            themes_directory.mkdir(exist_ok=True, parents=True)
            config_file.parent.mkdir(exist_ok=True, parents=True)
            
            logger.info(f"Base directory: {base_dir}")
            logger.info(f"Themes directory: {themes_directory}")
            logger.info(f"Config file: {config_file}")
            
            # Initialize managers
            self.config_manager = ConfigManager(config_file)
            self.theme_manager = ThemeManager(self.config_manager, themes_directory)
            self.ui_manager = UIManager()
            self.termux_integration = TermuxIntegration()
            
            # Load configuration
            if not self.config_manager.load_config():
                logger.warning("Failed to load config, using defaults")
            
            # Verify theme directory exists and has themes
            if not self.theme_manager.verify_themes_directory():
                logger.warning(f"Themes directory not found at {themes_directory}")
                print("Warning: No themes directory found. Creating default structure...")
                self._create_default_theme_structure(themes_directory)
                
            self.initialized = True
            logger.info("Application initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize application: {e}", exc_info=True)
            return False
    
    def _is_termux_environment(self) -> bool:
        """Check if we're running in Termux environment"""
        return os.path.exists('/data/data/com.termux/files/home')
    
    def _create_default_theme_structure(self, themes_dir: Path) -> None:
        """Create default theme structure if it doesn't exist"""
        try:
            # Create default theme
            default_theme_dir = themes_dir / "default"
            default_theme_dir.mkdir(exist_ok=True, parents=True)
            
            # Create default colors.properties
            colors_content = """# Termux Default Theme
background=#000000
foreground=#FFFFFF
cursor=#FFFFFF
color0=#000000
color1=#FF0000
color2=#00FF00
color3=#FFFF00
color4=#0000FF
color5=#FF00FF
color6=#00FFFF
color7=#FFFFFF
color8=#555555
color9=#FF5555
color10=#55FF55
color11=#FFFF55
color12=#5555FF
color13=#FF55FF
color14=#55FFFF
color15=#FFFFFF
"""
            with open(default_theme_dir / "colors.properties", "w") as f:
                f.write(colors_content)
            
            # Create default font.properties
            font_content = """# Termux Default Font
font=monospace
font-size=12
"""
            with open(default_theme_dir / "font.properties", "w") as f:
                f.write(font_content)
                
            # Create hacker theme
            hacker_theme_dir = themes_dir / "hacker"
            hacker_theme_dir.mkdir(exist_ok=True, parents=True)
            
            hacker_colors = """# Hacker Theme
background=#000000
foreground=#00FF00
cursor=#00FF00
color0=#000000
color1=#FF0000
color2=#00FF00
color3=#FFFF00
color4=#0000FF
color5=#FF00FF
color6=#00FFFF
color7=#FFFFFF
color8=#555555
color9=#FF5555
color10=#55FF55
color11=#FFFF55
color12=#5555FF
color13=#FF55FF
color14=#55FFFF
color15=#FFFFFF
"""
            with open(hacker_theme_dir / "colors.properties", "w") as f:
                f.write(hacker_colors)
            
            with open(hacker_theme_dir / "font.properties", "w") as f:
                f.write(font_content)
                
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
                    # Reload Termux session to apply changes
                    self.termux_integration.reload_termux_session()
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
                # Reload Termux session to apply changes
                self.termux_integration.reload_termux_session()
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
    
    def create_custom_theme(self) -> None:
        """Create a custom theme"""
        try:
            theme_name = self.ui_manager.get_theme_name("Enter name for new theme: ")
            if not theme_name:
                return
                
            if theme_name in self.theme_manager.list_themes():
                print(f"Theme '{theme_name}' already exists.")
                return
                
            # Get theme configuration from user
            print("\nCreating custom theme. Please provide the following information:")
            
            bg_color = input("Background color (hex, e.g., #000000): ").strip() or "#000000"
            fg_color = input("Foreground color (hex, e.g., #FFFFFF): ").strip() or "#FFFFFF"
            cursor_color = input("Cursor color (hex, e.g., #FFFFFF): ").strip() or "#FFFFFF"
            font_size = input("Font size (e.g., 12): ").strip() or "12"
            
            success, message = self.theme_manager.create_custom_theme(
                theme_name, bg_color, fg_color, cursor_color, font_size
            )
            
            if success:
                print(f"Custom theme '{theme_name}' created successfully!")
                print(message)
            else:
                print(f"Failed to create custom theme: {message}")
                
        except (KeyboardInterrupt, EOFError):
            print("\nCancelled.")
        except Exception as e:
            logger.error(f"Error creating custom theme: {e}")
            print(f"Error: Failed to create custom theme. {e}")
    
    def run(self) -> None:
        """Main application loop"""
        if not self.initialized:
            print("Application not properly initialized. Exiting.")
            return
            
        print("\n" + "="*50)
        print("      WELCOME TO TERMUX THEME CHANGER")
        print("="*50)
        print("Enhance your Termux terminal appearance!")
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
                    self.create_custom_theme()
                
                elif choice == '6':
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
    print("Initializing Termux Theme Changer...")
    
    app = TermuxThemeChanger()
    
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