from theme_manager import ThemeManager
from config_manager import ConfigManager
from ui_manager import UIManager

def main():
    themes_directory = "themes"
    default_theme_path = "config/default_theme"
    config_file = "config/config.ini"

    theme_manager = ThemeManager(themes_directory)
    config_manager = ConfigManager(config_file)
    ui_manager = UIManager()

    while True:
        ui_manager.display_menu()
        choice = ui_manager.get_user_choice()

        if choice == '1':
            themes = theme_manager.list_themes()
            print("Available Themes:")
            for theme in themes:
                print(f"- {theme}")
        elif choice == '2':
            theme_name = ui_manager.get_theme_name()
            theme_manager.apply_theme(theme_name)
        elif choice == '3':
            theme_manager.revert_to_default(default_theme_path)
        elif choice == '4':
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
