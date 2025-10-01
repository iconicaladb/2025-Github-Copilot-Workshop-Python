// Timer logic for Pomodoro Timer
let timerDuration = 25 * 60; // 25 minutes in seconds
let timeRemaining = timerDuration;
let timerInterval = null;

function formatTime(seconds) {
    const m = String(Math.floor(seconds / 60)).padStart(2, '0');
    const s = String(seconds % 60).padStart(2, '0');
    return `${m}:${s}`;
}

function updateTimerDisplay() {
    document.getElementById('timer').textContent = formatTime(timeRemaining);
    updateProgressBar();
}

function startTimer() {
    if (timerInterval) return;
    timerInterval = setInterval(() => {
        if (timeRemaining > 0) {
            timeRemaining--;
            updateTimerDisplay();
        } else {
            clearInterval(timerInterval);
            timerInterval = null;
            handleSessionComplete();
        }
    }, 1000);
}

function resetTimer() {
    clearInterval(timerInterval);
    timerInterval = null;
    timeRemaining = timerDuration;
    updateTimerDisplay();
}

async function handleSessionComplete() {
    // Notify gamification system
    if (window.gamification) {
        const result = await window.gamification.onSessionComplete();
        if (result) {
            // Show completion notification with XP gained
            showSessionCompleteNotification(result);
        }
    } else {
        // Fallback if gamification not loaded
        alert('Session Complete!');
    }
    
    // Reset timer for next session
    timeRemaining = timerDuration;
    updateTimerDisplay();
}

function showSessionCompleteNotification(result) {
    // Create a temporary notification for session completion
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #7b6ef6 0%, #a8a1f7 100%);
        color: white;
        padding: 16px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(123, 110, 246, 0.3);
        z-index: 1000;
        font-weight: bold;
        animation: slideIn 0.3s ease;
    `;
    
    notification.innerHTML = `
        <div style="display: flex; align-items: center; gap: 12px;">
            <span style="font-size: 1.5rem;">🍅</span>
            <div>
                <div>Session Complete!</div>
                <div style="font-size: 0.9rem; opacity: 0.9;">+${result.xp_gained} XP</div>
            </div>
        </div>
    `;
    
    // Add slide in animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
    `;
    document.head.appendChild(style);
    
    document.body.appendChild(notification);
    
    // Remove notification after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideIn 0.3s ease reverse';
        setTimeout(() => {
            document.body.removeChild(notification);
            document.head.removeChild(style);
        }, 300);
    }, 3000);
}

function updateProgressBar() {
    const percent = (timerDuration - timeRemaining) / timerDuration;
    const circle = document.getElementById('progress-circle');
    const radius = circle.r.baseVal.value;
    const circumference = 2 * Math.PI * radius;
    circle.style.strokeDasharray = `${circumference}`;
    circle.style.strokeDashoffset = `${circumference * (1 - percent)}`;
}

document.getElementById('start-btn').addEventListener('click', startTimer);
document.getElementById('reset-btn').addEventListener('click', resetTimer);

document.addEventListener('DOMContentLoaded', () => {
    updateTimerDisplay();
});
