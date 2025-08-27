from theme_manager import ThemeManager
from config_manager import ConfigManager
from ui_manager import UIManager

def main():
    # Setup paths
    themes_directory = "themes"
    default_theme_path = "themes/default"  # corrected path
    config_file = "config/config.ini"

    # Initialize managers
    theme_manager = ThemeManager(themes_directory)
    config_manager = ConfigManager(config_file)
    ui_manager = UIManager()

    while True:
        ui_manager.display_menu()
        choice = ui_manager.get_user_choice()

        if choice == '1':
            themes = theme_manager.list_themes()
            print("\nAvailable Themes:")
            for theme in themes:
                print(f"- {theme}")
            print()
        
        elif choice == '2':
            theme_name = ui_manager.get_theme_name()
            themes = theme_manager.list_themes()
            
            if theme_name in themes:
                theme_manager.apply_theme(theme_name)
                print(f"Theme '{theme_name}' applied successfully.\n")
                
                # Optional: save to config
                # config_manager.set_config("theme", "current", theme_name)
            else:
                print(f"Theme '{theme_name}' not found. Please try again.\n")
        
        elif choice == '3':
            theme_manager.revert_to_default(default_theme_path)
            print("Reverted to default theme.\n")

        elif choice == '4':
            print("Exiting... Goodbye!")
            break

        else:
            print("Invalid choice, please try again.\n")

if __name__ == "__main__":
    main()