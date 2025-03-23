import os
import shutil
import logging
import yaml

class ThemeManager:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        self.themes_directory = self.config['themes_directory']
        self.default_theme_path = self.config['default_theme_path']
        self.backup_directory = os.path.expanduser("~/.termux_backup")

        logging.basicConfig(filename='theme_manager.log', level=logging.INFO)

    def load_config(self, config_path):
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)

    def list_themes(self):
        try:
            themes = [theme for theme in os.listdir(self.themes_directory) if os.path.isdir(os.path.join(self.themes_directory, theme))]
            logging.info(f"Listed themes: {themes}")
            return themes
        except Exception as e:
            logging.error(f"Error listing themes: {e}")
            print(f"Error listing themes: {e}")
            return []

    def apply_theme(self, theme_name):
        theme_path = os.path.join(self.themes_directory, theme_name)
        if os.path.exists(theme_path):
            try:
                self.backup_current_theme()
                shutil.copytree(theme_path, os.path.expanduser("~/.termux"), dirs_exist_ok=True)
                logging.info(f"Theme '{theme_name}' applied successfully.")
                print(f"Theme '{theme_name}' applied successfully.")
            except Exception as e:
                logging.error(f"Error applying theme '{theme_name}': {e}")
                print(f"Error applying theme '{theme_name}': {e}")
        else:
            logging.warning(f"Theme '{theme_name}' does not exist.")
            print(f"Theme '{theme_name}' does not exist.")

    def revert_to_default(self):
        try:
            shutil.copytree(self.default_theme_path, os.path.expanduser("~/.termux"), dirs_exist_ok=True)
            logging.info("Reverted to default theme.")
            print("Reverted to default theme.")
        except Exception as e:
            logging.error(f"Error reverting to default theme: {e}")
            print(f"Error reverting to default theme: {e}")

    def backup_current_theme(self):
        current_theme_path = os.path.expanduser("~/.termux")
        if os.path.exists(current_theme_path):
            try:
                if os.path.exists(self.backup_directory):
                    shutil.rmtree(self.backup_directory)
                shutil.copytree(current_theme_path, self.backup_directory)
                logging.info("Current theme backed up successfully.")
                print("Current theme backed up successfully.")
            except Exception as e:
                logging.error(f"Error backing up current theme: {e}")
                print(f"Error backing up current theme: {e}")

# Configuration file (config.yaml)
"""
themes_directory: "/path/to/themes"
default_theme_path: "/path/to/default/theme"
"""
