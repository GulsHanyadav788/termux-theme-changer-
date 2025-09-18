import os
import sys
from pathlib import Path
from typing import List, Optional

# Import local modules
try:
    from theme_manager import ThemeManager
    from config_manager import ConfigManager
    from ui_manager import UIManager
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Please ensure all required modules are available.")
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
            base_dir = Path(__file__).parent
            themes_directory = base_dir / "themes"
            default_theme_path = themes_directory / "default"
            config_file = base_dir / "config" / "config.yaml"
            
            # Ensure directories exist
            themes_directory.mkdir(exist_ok=True)
            config_file.parent.mkdir(exist_ok=True)
            
            # Initialize managers
            self.theme_manager = ThemeManager(config_file, themes_directory, default_theme_path)
            self.ui_manager = UIManager()
            self.config_manager = ConfigManager(config_file)
            
            # Verify theme directory exists and has themes
            if not self.theme_manager.verify_themes_directory():
                print(f"Warning: Themes directory not found at {themes_directory}")
                print("Please create a 'themes' directory with some themes.")
                return False
                
            self.initialized = True
            return True
            
        except Exception as e:
            print(f"Failed to initialize application: {e}")
            return False
    
    def display_available_themes(self) -> None:
        """Display all available themes"""
        try:
            themes = self.theme_manager.list_themes()
            if not themes:
                print("No themes available. Please add some themes to the themes directory.")
                return
                
            print("\nAvailable Themes:")
            for i, theme in enumerate(themes, 1):
                print(f"{i}. {theme}")
            print()
            
        except Exception as e:
            print(f"Error listing themes: {e}")
    
    def apply_selected_theme(self) -> None:
        """Apply a theme selected by the user"""
        try:
            themes = self.theme_manager.list_themes()
            if not themes:
                print("No themes available to apply.")
                return
                
            self.display_available_themes()
            theme_name = self.ui_manager.get_theme_name()
            
            if theme_name in themes:
                success = self.theme_manager.apply_theme(theme_name)
                if success:
                    print(f"Theme '{theme_name}' applied successfully!\n")
                else:
                    print(f"Failed to apply theme '{theme_name}'.\n")
            else:
                print(f"Theme '{theme_name}' not found. Please try again.\n")
                
        except Exception as e:
            print(f"Error applying theme: {e}")
    
    def revert_to_default_theme(self) -> None:
        """Revert to the default theme"""
        try:
            success = self.theme_manager.revert_to_default()
            if success:
                print("Reverted to default theme successfully!\n")
            else:
                print("Failed to revert to default theme.\n")
        except Exception as e:
            print(f"Error reverting to default theme: {e}")
    
    def run(self) -> None:
        """Main application loop"""
        if not self.initialized:
            print("Application not properly initialized. Exiting.")
            return
            
        print("Welcome to Termex Theme Changer!")
        
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
                    print("Exiting... Goodbye!")
                    break
                
                else:
                    print("Invalid choice, please try again.\n")
                    
            except KeyboardInterrupt:
                print("\n\nInterrupted by user. Exiting...")
                break
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                print("Please try again.\n")


def main():
    """Main entry point for the application"""
    app = TermexThemeChanger()
    
    if not app.initialize():
        print("Failed to initialize application. Exiting.")
        return 1
        
    try:
        app.run()
    except Exception as e:
        print(f"Unexpected error in application: {e}")
        return 1
        
    return 0


if __name__ == "__main__":
    sys.exit(main())