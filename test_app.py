import unittest
import json
import tempfile
import os
from app import app

class TestPomodoroApp(unittest.TestCase):
    def setUp(self):
        # Create a temporary file for gamification data
        self.temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json')
        self.temp_file.close()
        
        app.config['TESTING'] = True
        self.app = app.test_client()
        
        # Monkey patch the gamification manager to use temp file
        from app import gamification
        gamification.data_file = self.temp_file.name
        gamification.reset_stats()

    def tearDown(self):
        # Clean up temporary file
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Pomodoro Timer', response.data)
        self.assertIn(b'Start', response.data)
        self.assertIn(b'Reset', response.data)
        self.assertIn(b"Today's Progress", response.data)
        self.assertIn(b'Focus Time', response.data)
        # Test new gamification elements
        self.assertIn(b'Level', response.data)
        self.assertIn(b'Achievements', response.data)
        self.assertIn(b'Statistics', response.data)

    def test_get_stats_api(self):
        response = self.app.get('/api/stats')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('total_xp', data)
        self.assertIn('level', data)
        self.assertIn('total_sessions', data)
        self.assertIn('current_streak', data)
        self.assertIn('achievements', data)
        self.assertIn('weekly_sessions', data)
        self.assertIn('monthly_sessions', data)
        
        # Initial stats should be zero
        self.assertEqual(data['total_xp'], 0)
        self.assertEqual(data['level'], 1)
        self.assertEqual(data['total_sessions'], 0)

    def test_complete_session_api(self):
        response = self.app.post('/api/complete-session')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('xp_gained', data)
        self.assertIn('total_xp', data)
        self.assertIn('level', data)
        self.assertIn('current_streak', data)
        self.assertIn('new_achievements', data)
        
        # First session should gain 25 XP and unlock first achievement
        self.assertEqual(data['xp_gained'], 25)
        self.assertEqual(data['total_xp'], 25)
        self.assertEqual(data['level'], 1)
        self.assertEqual(data['current_streak'], 1)
        self.assertEqual(len(data['new_achievements']), 1)
        self.assertEqual(data['new_achievements'][0]['id'], 'first_completion')

    def test_reset_stats_api(self):
        # Complete a session first
        self.app.post('/api/complete-session')
        
        # Reset stats
        response = self.app.post('/api/reset-stats')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('message', data)
        
        # Verify stats are reset
        response = self.app.get('/api/stats')
        stats = json.loads(response.data)
        self.assertEqual(stats['total_xp'], 0)
        self.assertEqual(stats['total_sessions'], 0)

    def test_multiple_sessions(self):
        """Test multiple session completions"""
        # Complete 3 sessions
        for i in range(3):
            response = self.app.post('/api/complete-session')
            self.assertEqual(response.status_code, 200)
        
        # Check final stats
        response = self.app.get('/api/stats')
        data = json.loads(response.data)
        
        self.assertEqual(data['total_xp'], 75)  # 25 XP * 3 sessions
        self.assertEqual(data['total_sessions'], 3)
        self.assertEqual(data['level'], 1)  # Still level 1 (need 100 XP for level 2)

if __name__ == '__main__':
    unittest.main()
