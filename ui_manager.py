"""
UI Manager for Termux Theme Changer
Handles user interface and input
"""

import os
import sys
from typing import Optional
import logging

logger = logging.getLogger("termux_theme_changer.ui_manager")


class UIManager:
    """Manages user interface and input"""
    
    def display_menu(self) -> None:
        """Display the main menu"""
        print("\n" + "="*30)
        print("     TERMUX THEME CHANGER")
        print("="*30)
        print("1. List available themes")
        print("2. Apply a theme")
        print("3. Revert to default theme")
        print("4. Show current theme")
        print("5. Create custom theme")
        print("6. Exit")
        print("="*30)
    
    def get_user_choice(self) -> str:
        """Get user choice from menu"""
        try:
            choice = input("\nPlease enter your choice (1-6): ").strip()
            return choice
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            sys.exit(0)
        except Exception as e:
            logger.error(f"Error getting user choice: {e}")
            return ""
    
    def get_theme_name(self, prompt: str = "Enter the theme name: ") -> Optional[str]:
        """Get theme name from user"""
        try:
            theme_name = input(prompt).strip()
            return theme_name if theme_name else None
        except (EOFError, KeyboardInterrupt):
            print("\nCancelled.")
            return None
        except Exception as e:
            logger.error(f"Error getting theme name: {e}")
            return None
    
    def display_message(self, message: str) -> None:
        """Display a message to the user"""
        print(f"\n{message}")
    
    def display_error(self, error: str) -> None:
        """Display an error message to the user"""
        print(f"\nERROR: {error}", file=sys.stderr)
    
    def get_yes_no_input(self, prompt: str) -> bool:
        """Get yes/no input from user"""
        try:
            response = input(f"{prompt} (y/n): ").strip().lower()
            return response in ['y', 'yes']
        except (EOFError, KeyboardInterrupt):
            print("\nCancelled.")
            return False
        except Exception as e:
            logger.error(f"Error getting yes/no input: {e}")
            return False