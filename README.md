# 🍅 Pomodoro Timer with Gamification

A modern, gamified Pomodoro timer web application built with Flask and JavaScript. Features a comprehensive XP system, achievements, streak tracking, and statistics to boost motivation and encourage consistent use.

## 🎮 Gamification Features

### XP System & Leveling
- **25 XP** earned per completed Pomodoro session
- **100 XP** required per level advancement
- Visual XP progress bar in the header
- Level up notifications with celebration modals

### Achievement System (7 Total)
- 🍅 **First Steps**: Complete your first Pomodoro session
- 🔥 **Consistent**: Complete sessions for 3 consecutive days
- ⚡ **Dedicated**: Complete sessions for 7 consecutive days  
- 💪 **Weekly Warrior**: Complete 10 sessions in a week
- 👑 **Focus Master**: Complete 20 sessions in a week
- 🏆 **Half Century**: Complete 50 total sessions
- 🌟 **Centurion**: Complete 100 total sessions

### Streak Tracking
- Daily streak counter with fire emoji 🔥
- Automatic streak continuation for consecutive days
- Streak reset after missing a day
- Best streak tracking for personal records

### Statistics & Analytics
- **Weekly View**: Last 8 weeks of session data
- **Monthly View**: Last 6 months of session data
- Interactive bar charts with hover effects
- Session completion trends over time

## 🚀 Features

- **Timer**: 25-minute Pomodoro sessions with visual countdown
- **Progress Tracking**: Daily session count and focus time
- **Gamification**: XP, levels, achievements, and streaks
- **Statistics**: Weekly and monthly analytics with charts
- **Visual Feedback**: Beautiful animations and notifications
- **Data Persistence**: All progress saved automatically
- **Responsive Design**: Works on desktop and mobile

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/iconicaladb/2025-Github-Copilot-Workshop-Python.git
cd 2025-Github-Copilot-Workshop-Python
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to `http://127.0.0.1:5000`

## 🧪 Testing

Run the test suite:
```bash
# Test gamification system
python test_gamification.py

# Test Flask app
python test_app.py
```

## 🏗️ Architecture

- **Backend**: Flask web framework with RESTful API endpoints
- **Frontend**: Vanilla JavaScript with modern ES6+ features
- **Data Storage**: JSON file-based persistence
- **Styling**: Custom CSS with gradients and animations
- **Testing**: Comprehensive unit and integration tests

## 📁 Project Structure

```
├── app.py                  # Flask application entry point
├── gamification.py         # Gamification system logic
├── templates/
│   └── index.html         # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css      # Application styles
│   └── js/
│       ├── timer.js       # Timer functionality
│       └── gamification.js # Gamification UI logic
├── test_app.py            # Flask app tests
├── test_gamification.py   # Gamification tests
└── data/
    └── gamification.json  # User data storage
```

## 🔌 API Endpoints

- `GET /` - Main application page
- `GET /api/stats` - Get current user statistics
- `POST /api/complete-session` - Mark a session as completed
- `POST /api/reset-stats` - Reset all statistics (for testing)

## 📊 Screenshots

| Original UI | Gamified UI | Achievement Modal |
|-------------|-------------|-------------------|
| ![Original](https://github.com/user-attachments/assets/a0fb6524-651e-4e66-9b76-c4315d9f20b9) | ![Gamified](https://github.com/user-attachments/assets/d7ad1178-8d0b-4840-8e42-bfb704289c62) | ![Achievement](https://github.com/user-attachments/assets/308852a9-b426-45b3-a9d1-2b64a1eb4194) |

**Level 2 Progress**: ![Level 2](https://github.com/user-attachments/assets/fe9f1feb-796f-4750-a228-d9f670961a61)

## 🎯 How It Works

1. **Start a Session**: Click the Start button to begin a 25-minute Pomodoro session
2. **Complete Sessions**: When the timer reaches zero, you earn 25 XP and update your streak
3. **Unlock Achievements**: Complete specific milestones to earn achievement badges
4. **Level Up**: Accumulate 100 XP to advance to the next level
5. **Track Progress**: View your statistics in weekly or monthly chart views
6. **Build Streaks**: Complete sessions on consecutive days to maintain your streak

## 🔮 Future Enhancements

Potential features for future development:
- User authentication and multiple profiles
- Custom session durations
- Break time tracking
- Sound notifications
- Dark mode theme
- Export statistics
- Social features and leaderboards

## 📝 Workshop Reference

ワークショップの手順：https://moulongzhang.github.io/2025-Github-Copilot-Workshop/github-copilot-workshop/#0

## 🤝 Contributing

This project was created as part of the 2025 GitHub Copilot Workshop to demonstrate AI-assisted development for adding gamification features to a Pomodoro timer application.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
