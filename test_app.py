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

if __name__ == '__main__':
    unittest.main()
