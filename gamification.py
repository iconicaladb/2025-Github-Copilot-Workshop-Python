# Gamification system for Pomodoro Timer
import json
import os
from datetime import datetime, date, timedelta
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from enum import Enum

class AchievementType(Enum):
    FIRST_COMPLETION = "first_completion"
    DAILY_STREAK_3 = "daily_streak_3"
    DAILY_STREAK_7 = "daily_streak_7"
    WEEKLY_10 = "weekly_10"
    WEEKLY_20 = "weekly_20"
    TOTAL_50 = "total_50"
    TOTAL_100 = "total_100"

@dataclass
class Achievement:
    id: str
    name: str
    description: str
    icon: str
    earned: bool = False
    earned_date: str = None

@dataclass
class UserStats:
    total_xp: int = 0
    level: int = 1
    total_sessions: int = 0
    current_streak: int = 0
    best_streak: int = 0
    last_session_date: str = None
    achievements: List[Dict] = None
    weekly_sessions: Dict[str, int] = None
    monthly_sessions: Dict[str, int] = None

    def __post_init__(self):
        if self.achievements is None:
            self.achievements = []
        if self.weekly_sessions is None:
            self.weekly_sessions = {}
        if self.monthly_sessions is None:
            self.monthly_sessions = {}

class GamificationManager:
    def __init__(self, data_file='data/gamification.json'):
        self.data_file = data_file
        self.achievements_definitions = {
            AchievementType.FIRST_COMPLETION: Achievement(
                "first_completion", "First Steps", "Complete your first Pomodoro session", "🍅"
            ),
            AchievementType.DAILY_STREAK_3: Achievement(
                "daily_streak_3", "Consistent", "Complete sessions for 3 consecutive days", "🔥"
            ),
            AchievementType.DAILY_STREAK_7: Achievement(
                "daily_streak_7", "Dedicated", "Complete sessions for 7 consecutive days", "⚡"
            ),
            AchievementType.WEEKLY_10: Achievement(
                "weekly_10", "Weekly Warrior", "Complete 10 sessions in a week", "💪"
            ),
            AchievementType.WEEKLY_20: Achievement(
                "weekly_20", "Focus Master", "Complete 20 sessions in a week", "👑"
            ),
            AchievementType.TOTAL_50: Achievement(
                "total_50", "Half Century", "Complete 50 total sessions", "🏆"
            ),
            AchievementType.TOTAL_100: Achievement(
                "total_100", "Centurion", "Complete 100 total sessions", "🌟"
            )
        }
        self.user_stats = self._load_stats()

    def _load_stats(self) -> UserStats:
        """Load user statistics from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                return UserStats(**data)
            except (json.JSONDecodeError, TypeError):
                pass
        return UserStats()

    def _save_stats(self):
        """Save user statistics to file"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(asdict(self.user_stats), f, indent=2)

    def _calculate_level(self, xp: int) -> int:
        """Calculate level based on XP (100 XP per level)"""
        return max(1, (xp // 100) + 1)

    def _get_week_key(self, date_obj: date = None) -> str:
        """Get week key in format YYYY-WW"""
        if date_obj is None:
            date_obj = date.today()
        year, week, _ = date_obj.isocalendar()
        return f"{year}-{week:02d}"

    def _get_month_key(self, date_obj: date = None) -> str:
        """Get month key in format YYYY-MM"""
        if date_obj is None:
            date_obj = date.today()
        return f"{date_obj.year}-{date_obj.month:02d}"

    def complete_session(self) -> Dict[str, Any]:
        """Handle session completion and return updated stats with new achievements"""
        today = date.today().isoformat()
        xp_gained = 25  # 25 XP per completed session
        
        # Update basic stats
        self.user_stats.total_xp += xp_gained
        self.user_stats.total_sessions += 1
        old_level = self.user_stats.level
        self.user_stats.level = self._calculate_level(self.user_stats.total_xp)
        
        # Update streak
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        if self.user_stats.last_session_date == yesterday:
            self.user_stats.current_streak += 1
        elif self.user_stats.last_session_date != today:  # New streak if not today
            self.user_stats.current_streak = 1
        
        self.user_stats.best_streak = max(self.user_stats.best_streak, self.user_stats.current_streak)
        self.user_stats.last_session_date = today
        
        # Update weekly/monthly stats
        week_key = self._get_week_key()
        month_key = self._get_month_key()
        self.user_stats.weekly_sessions[week_key] = self.user_stats.weekly_sessions.get(week_key, 0) + 1
        self.user_stats.monthly_sessions[month_key] = self.user_stats.monthly_sessions.get(month_key, 0) + 1
        
        # Check for new achievements
        new_achievements = self._check_achievements()
        
        # Save updated stats
        self._save_stats()
        
        return {
            'xp_gained': xp_gained,
            'total_xp': self.user_stats.total_xp,
            'level': self.user_stats.level,
            'level_up': self.user_stats.level > old_level,
            'current_streak': self.user_stats.current_streak,
            'new_achievements': new_achievements,
            'total_sessions': self.user_stats.total_sessions
        }

    def _check_achievements(self) -> List[Dict]:
        """Check and award new achievements"""
        new_achievements = []
        earned_ids = {ach['id'] for ach in self.user_stats.achievements}
        
        # Check each achievement type
        checks = [
            (AchievementType.FIRST_COMPLETION, self.user_stats.total_sessions >= 1),
            (AchievementType.DAILY_STREAK_3, self.user_stats.current_streak >= 3),
            (AchievementType.DAILY_STREAK_7, self.user_stats.current_streak >= 7),
            (AchievementType.WEEKLY_10, max(self.user_stats.weekly_sessions.values(), default=0) >= 10),
            (AchievementType.WEEKLY_20, max(self.user_stats.weekly_sessions.values(), default=0) >= 20),
            (AchievementType.TOTAL_50, self.user_stats.total_sessions >= 50),
            (AchievementType.TOTAL_100, self.user_stats.total_sessions >= 100),
        ]
        
        for achievement_type, condition in checks:
            achievement_def = self.achievements_definitions[achievement_type]
            if condition and achievement_def.id not in earned_ids:
                earned_achievement = asdict(achievement_def)
                earned_achievement['earned'] = True
                earned_achievement['earned_date'] = date.today().isoformat()
                self.user_stats.achievements.append(earned_achievement)
                new_achievements.append(earned_achievement)
        
        return new_achievements

    def get_stats(self) -> Dict[str, Any]:
        """Get current user statistics"""
        return {
            'total_xp': self.user_stats.total_xp,
            'level': self.user_stats.level,
            'xp_to_next_level': 100 - (self.user_stats.total_xp % 100),
            'total_sessions': self.user_stats.total_sessions,
            'current_streak': self.user_stats.current_streak,
            'best_streak': self.user_stats.best_streak,
            'achievements': self.user_stats.achievements,
            'weekly_sessions': self._get_recent_weekly_stats(),
            'monthly_sessions': self._get_recent_monthly_stats(),
        }

    def _get_recent_weekly_stats(self) -> List[Dict]:
        """Get last 8 weeks of session data"""
        weeks = []
        for i in range(7, -1, -1):  # Last 8 weeks including current
            week_date = date.today() - timedelta(weeks=i)
            week_key = self._get_week_key(week_date)
            sessions = self.user_stats.weekly_sessions.get(week_key, 0)
            weeks.append({
                'week': week_key,
                'sessions': sessions,
                'label': f"Week {week_date.isocalendar()[1]}"
            })
        return weeks

    def _get_recent_monthly_stats(self) -> List[Dict]:
        """Get last 6 months of session data"""
        months = []
        for i in range(5, -1, -1):  # Last 6 months including current
            month_date = date.today().replace(day=1) - timedelta(days=i*30)
            month_key = self._get_month_key(month_date)
            sessions = self.user_stats.monthly_sessions.get(month_key, 0)
            months.append({
                'month': month_key,
                'sessions': sessions,
                'label': month_date.strftime('%b %Y')
            })
        return months

    def reset_stats(self):
        """Reset all statistics (for testing purposes)"""
        self.user_stats = UserStats()
        self._save_stats()