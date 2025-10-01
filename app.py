# Flask app entry point for Pomodoro Timer

from flask import Flask, render_template, jsonify, request
from gamification import GamificationManager

app = Flask(__name__)
gamification = GamificationManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stats')
def get_stats():
    """Get current user statistics"""
    return jsonify(gamification.get_stats())

@app.route('/api/complete-session', methods=['POST'])
def complete_session():
    """Mark a session as completed and update gamification stats"""
    result = gamification.complete_session()
    return jsonify(result)

@app.route('/api/reset-stats', methods=['POST'])
def reset_stats():
    """Reset all statistics (for testing purposes)"""
    gamification.reset_stats()
    return jsonify({'message': 'Stats reset successfully'})

if __name__ == '__main__':
    app.run(debug=True)
