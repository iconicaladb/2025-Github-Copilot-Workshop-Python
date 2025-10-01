import unittest
import json
import os
import tempfile
from datetime import date, timedelta
from gamification import GamificationManager, AchievementType

class TestGamificationManager(unittest.TestCase):
    def setUp(self):
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json')
        self.temp_file.close()
        self.gamification = GamificationManager(data_file=self.temp_file.name)

    def tearDown(self):
        # Clean up temporary file
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_initial_stats(self):
        """Test initial user statistics"""
        stats = self.gamification.get_stats()
        self.assertEqual(stats['total_xp'], 0)
        self.assertEqual(stats['level'], 1)
        self.assertEqual(stats['xp_to_next_level'], 100)
        self.assertEqual(stats['total_sessions'], 0)
        self.assertEqual(stats['current_streak'], 0)
        self.assertEqual(stats['best_streak'], 0)
        self.assertEqual(len(stats['achievements']), 0)

    def test_complete_session_basic(self):
        """Test basic session completion"""
        result = self.gamification.complete_session()
        
        self.assertEqual(result['xp_gained'], 25)
        self.assertEqual(result['total_xp'], 25)
        self.assertEqual(result['level'], 1)
        self.assertFalse(result['level_up'])
        self.assertEqual(result['current_streak'], 1)
        self.assertEqual(result['total_sessions'], 1)
        
        # Should get first completion achievement
        self.assertEqual(len(result['new_achievements']), 1)
        self.assertEqual(result['new_achievements'][0]['id'], 'first_completion')

    def test_level_up(self):
        """Test level up functionality"""
        # Complete 4 sessions to get 100 XP and level up
        for i in range(4):
            result = self.gamification.complete_session()
        
        self.assertEqual(result['total_xp'], 100)
        self.assertEqual(result['level'], 2)
        self.assertTrue(result['level_up'])

    def test_streak_tracking(self):
        """Test streak tracking across days"""
        # First session today
        result1 = self.gamification.complete_session()
        self.assertEqual(result1['current_streak'], 1)
        
        # Simulate session yesterday by manually setting last session date
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        self.gamification.user_stats.last_session_date = yesterday
        
        result2 = self.gamification.complete_session()
        self.assertEqual(result2['current_streak'], 2)
        
        # Simulate gap of more than 1 day - streak should reset
        three_days_ago = (date.today() - timedelta(days=3)).isoformat()
        self.gamification.user_stats.last_session_date = three_days_ago
        
        result3 = self.gamification.complete_session()
        self.assertEqual(result3['current_streak'], 1)

    def test_achievement_progression(self):
        """Test various achievement unlocks"""
        # First completion
        result1 = self.gamification.complete_session()
        achievement_ids = [ach['id'] for ach in result1['new_achievements']]
        self.assertIn('first_completion', achievement_ids)
        
        # Simulate 3-day streak achievement
        self.gamification.user_stats.current_streak = 3
        result2 = self.gamification.complete_session()
        achievement_ids = [ach['id'] for ach in result2['new_achievements']]
        self.assertIn('daily_streak_3', achievement_ids)

    def test_weekly_stats(self):
        """Test weekly statistics tracking"""
        # Complete multiple sessions
        for i in range(5):
            self.gamification.complete_session()
        
        stats = self.gamification.get_stats()
        weekly_sessions = stats['weekly_sessions']
        
        # Should have data for current week
        current_week_sessions = max(week['sessions'] for week in weekly_sessions)
        self.assertEqual(current_week_sessions, 5)

    def test_data_persistence(self):
        """Test that data persists across manager instances"""
        # Complete a session
        self.gamification.complete_session()
        
        # Create a new manager instance with the same file
        new_gamification = GamificationManager(data_file=self.temp_file.name)
        stats = new_gamification.get_stats()
        
        self.assertEqual(stats['total_sessions'], 1)
        self.assertEqual(stats['total_xp'], 25)
        self.assertEqual(len(stats['achievements']), 1)

    def test_reset_stats(self):
        """Test statistics reset functionality"""
        # Complete some sessions
        for i in range(3):
            self.gamification.complete_session()
        
        # Reset stats
        self.gamification.reset_stats()
        
        stats = self.gamification.get_stats()
        self.assertEqual(stats['total_xp'], 0)
        self.assertEqual(stats['level'], 1)
        self.assertEqual(stats['total_sessions'], 0)
        self.assertEqual(stats['current_streak'], 0)
        self.assertEqual(len(stats['achievements']), 0)

if __name__ == '__main__':
    unittest.main()