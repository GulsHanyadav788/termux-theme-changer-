class UIManager:
    def display_menu(self):
        print("Termux Theme Changer")
        print("1. List Themes")
        print("2. Apply Theme")
        print("3. Revert to Default")
        print("4. Exit")

    def get_user_choice(self):
        return input("Enter your choice: ")

    def get_theme_name(self):
        return input("Enter the theme name: ")
