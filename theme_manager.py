import os
import shutil

class ThemeManager:
    def __init__(self, themes_directory):
        self.themes_directory = themes_directory

    def list_themes(self):
        return [theme for theme in os.listdir(self.themes_directory) if os.path.isdir(os.path.join(self.themes_directory, theme))]

    def apply_theme(self, theme_name):
        theme_path = os.path.join(self.themes_directory, theme_name)
        if os.path.exists(theme_path):
            shutil.copytree(theme_path, os.path.expanduser("~/.termux"), dirs_exist_ok=True)
            print(f"Theme '{theme_name}' applied successfully.")
        else:
            print(f"Theme '{theme_name}' does not exist.")

    def revert_to_default(self, default_theme_path):
        shutil.copytree(default_theme_path, os.path.expanduser("~/.termux"), dirs_exist_ok=True)
        print("Reverted to default theme.")
