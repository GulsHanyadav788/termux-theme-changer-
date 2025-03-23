# tests/test_theme_manager.py
import unittest
from src.theme_manager import ThemeManager

class TestThemeManager(unittest.TestCase):

    def setUp(self):
        self.manager = ThemeManager()

    def test_add_theme(self):
        self.assertTrue(self.manager.add_theme('Dark'))
        self.assertIn('Dark', self.manager.list_themes())

    def test_add_duplicate_theme(self):
        self.manager.add_theme('Dark')
        self.assertFalse(self.manager.add_theme('Dark'))

    def test_remove_theme(self):
        self.manager.add_theme('Dark')
        self.assertTrue(self.manager.remove_theme('Dark'))
        self.assertNotIn('Dark', self.manager.list_themes())

    def test_remove_nonexistent_theme(self):
        self.assertFalse(self.manager.remove_theme('Nonexistent'))

    def test_list_themes(self):
        self.manager.add_theme('Dark')
        self.manager.add_theme('Light')
        self.assertEqual(self.manager.list_themes(), ['Dark', 'Light'])

if __name__ == '__main__':
    unittest.main()
