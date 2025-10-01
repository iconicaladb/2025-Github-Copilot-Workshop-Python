// Gamification module for Pomodoro Timer
class GamificationUI {
    constructor() {
        this.currentTab = 'weekly';
        this.stats = null;
        this.init();
    }

    async init() {
        this.bindEvents();
        await this.loadStats();
        this.updateUI();
    }

    bindEvents() {
        // Stats tab switching
        document.querySelectorAll('.stats-tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                const tabName = e.target.dataset.tab;
                this.switchTab(tabName);
            });
        });

        // Modal close events
        document.getElementById('close-modal')?.addEventListener('click', () => {
            this.hideAchievementModal();
        });

        document.getElementById('close-levelup-modal')?.addEventListener('click', () => {
            this.hideLevelUpModal();
        });

        // Click outside modal to close
        document.getElementById('achievement-modal')?.addEventListener('click', (e) => {
            if (e.target.id === 'achievement-modal') {
                this.hideAchievementModal();
            }
        });

        document.getElementById('levelup-modal')?.addEventListener('click', (e) => {
            if (e.target.id === 'levelup-modal') {
                this.hideLevelUpModal();
            }
        });
    }

    async loadStats() {
        try {
            const response = await fetch('/api/stats');
            this.stats = await response.json();
        } catch (error) {
            console.error('Failed to load stats:', error);
            this.stats = {
                total_xp: 0,
                level: 1,
                xp_to_next_level: 100,
                total_sessions: 0,
                current_streak: 0,
                best_streak: 0,
                achievements: [],
                weekly_sessions: [],
                monthly_sessions: []
            };
        }
    }

    updateUI() {
        if (!this.stats) return;

        // Update level and XP
        document.getElementById('user-level').textContent = this.stats.level;
        document.getElementById('user-xp').textContent = `${this.stats.total_xp} XP`;
        
        // Update XP progress bar
        const xpProgress = ((100 - this.stats.xp_to_next_level) / 100) * 100;
        document.getElementById('xp-progress').style.width = `${xpProgress}%`;

        // Update streak
        document.getElementById('current-streak').textContent = this.stats.current_streak;

        // Update basic progress
        document.getElementById('sessions-completed').textContent = `${this.stats.total_sessions} Completed`;
        const focusTime = this.calculateFocusTime(this.stats.total_sessions);
        document.getElementById('focus-time').textContent = focusTime;

        // Update achievements
        this.updateAchievements();

        // Update statistics chart
        this.updateChart();
    }

    calculateFocusTime(sessions) {
        const totalMinutes = sessions * 25; // 25 minutes per session
        const hours = Math.floor(totalMinutes / 60);
        const minutes = totalMinutes % 60;
        return `${hours}h ${minutes}m`;
    }

    updateAchievements() {
        const grid = document.getElementById('achievements-grid');
        if (!grid) return;

        // Define all possible achievements
        const allAchievements = [
            { id: 'first_completion', name: 'First Steps', description: 'Complete your first Pomodoro', icon: '🍅' },
            { id: 'daily_streak_3', name: 'Consistent', description: '3 day streak', icon: '🔥' },
            { id: 'daily_streak_7', name: 'Dedicated', description: '7 day streak', icon: '⚡' },
            { id: 'weekly_10', name: 'Weekly Warrior', description: '10 sessions in a week', icon: '💪' },
            { id: 'weekly_20', name: 'Focus Master', description: '20 sessions in a week', icon: '👑' },
            { id: 'total_50', name: 'Half Century', description: '50 total sessions', icon: '🏆' },
            { id: 'total_100', name: 'Centurion', description: '100 total sessions', icon: '🌟' }
        ];

        const earnedIds = new Set(this.stats.achievements.map(ach => ach.id));

        grid.innerHTML = allAchievements.map(achievement => {
            const earned = earnedIds.has(achievement.id);
            return `
                <div class="achievement ${earned ? 'earned' : ''}" title="${achievement.description}">
                    <div class="achievement-icon">${achievement.icon}</div>
                    <div class="achievement-name">${achievement.name}</div>
                </div>
            `;
        }).join('');
    }

    updateChart() {
        const chartContainer = document.getElementById('stats-chart');
        if (!chartContainer) return;

        const data = this.currentTab === 'weekly' ? this.stats.weekly_sessions : this.stats.monthly_sessions;
        const maxSessions = Math.max(...data.map(item => item.sessions), 1);

        chartContainer.innerHTML = data.map(item => {
            const height = (item.sessions / maxSessions) * 80; // Max height 80px
            return `
                <div class="chart-bar" style="height: ${height}px;">
                    <div class="chart-value">${item.sessions}</div>
                    <div class="chart-label">${item.label}</div>
                </div>
            `;
        }).join('');
    }

    switchTab(tabName) {
        this.currentTab = tabName;
        
        // Update tab buttons
        document.querySelectorAll('.stats-tab').forEach(tab => {
            tab.classList.toggle('active', tab.dataset.tab === tabName);
        });

        // Update chart
        this.updateChart();
    }

    async onSessionComplete() {
        try {
            const response = await fetch('/api/complete-session', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            const result = await response.json();
            
            // Reload stats and update UI
            await this.loadStats();
            this.updateUI();

            // Show notifications
            if (result.level_up) {
                this.showLevelUpModal(result.level);
            }

            if (result.new_achievements && result.new_achievements.length > 0) {
                // Show achievement modal for first new achievement
                setTimeout(() => {
                    this.showAchievementModal(result.new_achievements[0]);
                }, result.level_up ? 2000 : 0); // Delay if there was a level up
            }

            return result;
        } catch (error) {
            console.error('Failed to complete session:', error);
            return null;
        }
    }

    showAchievementModal(achievement) {
        const modal = document.getElementById('achievement-modal');
        const icon = document.getElementById('modal-achievement-icon');
        const name = document.getElementById('modal-achievement-name');
        const desc = document.getElementById('modal-achievement-desc');

        if (modal && icon && name && desc) {
            icon.textContent = achievement.icon;
            name.textContent = achievement.name;
            desc.textContent = achievement.description;
            modal.classList.remove('hidden');
        }
    }

    hideAchievementModal() {
        const modal = document.getElementById('achievement-modal');
        if (modal) {
            modal.classList.add('hidden');
        }
    }

    showLevelUpModal(level) {
        const modal = document.getElementById('levelup-modal');
        const levelSpan = document.getElementById('modal-new-level');

        if (modal && levelSpan) {
            levelSpan.textContent = level;
            modal.classList.remove('hidden');
        }
    }

    hideLevelUpModal() {
        const modal = document.getElementById('levelup-modal');
        if (modal) {
            modal.classList.add('hidden');
        }
    }
}

// Initialize gamification system when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.gamification = new GamificationUI();
});