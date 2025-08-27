from theme_manager import ThemeManager
from config_manager import ConfigManager
from ui_manager import UIManager

def main():
    themes_directory = "themes"
    default_theme_path = "themes/default"  # Correct path
    config_file = "config/config.yaml"     # YAML config

    theme_manager = ThemeManager(config_file)
    config_manager = ConfigManager("config/config.ini")  # if you want to use this elsewhere
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
            else:
                print(f"Theme '{theme_name}' not found. Please try again.\n")
        
        elif choice == '3':
            theme_manager.revert_to_default()  # No argument here
        
        elif choice == '4':
            print("Exiting... Goodbye!")
            break
        
        else:
            print("Invalid choice, please try again.\n")

if __name__ == "__main__":
    main()