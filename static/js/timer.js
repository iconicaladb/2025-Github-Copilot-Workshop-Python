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

function handleSessionComplete() {
    // TODO: Notify backend, update progress, show notification
    alert('Session Complete!');
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
