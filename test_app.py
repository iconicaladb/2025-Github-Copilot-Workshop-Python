import unittest
from app import app

class TestPomodoroApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Pomodoro Timer', response.data)
        self.assertIn(b'Start', response.data)
        self.assertIn(b'Reset', response.data)
        self.assertIn(b"Today's Progress", response.data)
        self.assertIn(b'Focus Time', response.data)
    
    def test_settings_modal_elements(self):
        """Test that the settings modal and customization elements are present"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        
        # Check for settings button
        self.assertIn(b'settings-btn', response.data)
        
        # Check for settings modal
        self.assertIn(b'settings-modal', response.data)
        
        # Check for time options
        self.assertIn(b'data-time="15"', response.data)
        self.assertIn(b'data-time="25"', response.data)
        self.assertIn(b'data-time="35"', response.data)
        self.assertIn(b'data-time="45"', response.data)
        
        # Check for theme options  
        self.assertIn(b'data-theme="light"', response.data)
        self.assertIn(b'data-theme="dark"', response.data)
        self.assertIn(b'data-theme="focus"', response.data)
        
        # Check for sound settings
        self.assertIn(b'start-sound', response.data)
        self.assertIn(b'end-sound', response.data)
        self.assertIn(b'tick-sound', response.data)

if __name__ == '__main__':
    unittest.main()
