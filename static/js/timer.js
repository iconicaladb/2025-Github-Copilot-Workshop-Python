// Timer logic for Pomodoro Timer with customization
let settings = {
    focusTime: 25,
    breakTime: 5,
    theme: 'dark',
    sounds: {
        start: true,
        end: true,
        tick: false
    }
};

let timerDuration = settings.focusTime * 60; // Default 25 minutes in seconds
let timeRemaining = timerDuration;
let timerInterval = null;
let isBreak = false;

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
    
    // Play start sound if enabled
    if (settings.sounds.start) {
        playSound('start');
    }
    
    timerInterval = setInterval(() => {
        if (timeRemaining > 0) {
            timeRemaining--;
            
            // Play tick sound if enabled
            if (settings.sounds.tick) {
                playSound('tick');
            }
            
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
    // Play end sound if enabled
    if (settings.sounds.end) {
        playSound('end');
    }
    
    if (!isBreak) {
        // Focus session complete, start break
        alert('Focus session complete! Time for a break.');
        startBreak();
    } else {
        // Break complete, return to focus
        alert('Break complete! Ready for another focus session?');
        isBreak = false;
        timerDuration = settings.focusTime * 60;
        timeRemaining = timerDuration;
        updateTimerDisplay();
    }
}

function startBreak() {
    isBreak = true;
    timerDuration = settings.breakTime * 60;
    timeRemaining = timerDuration;
    updateTimerDisplay();
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
    loadSettings();
    applyTheme();
    updateTimerDisplay();
    initializeSettingsPanel();
});

// Settings Management
function loadSettings() {
    const savedSettings = localStorage.getItem('pomodoroSettings');
    if (savedSettings) {
        settings = { ...settings, ...JSON.parse(savedSettings) };
        timerDuration = settings.focusTime * 60;
        timeRemaining = timerDuration;
    }
}

function saveSettings() {
    localStorage.setItem('pomodoroSettings', JSON.stringify(settings));
}

function applyTheme() {
    document.body.className = settings.theme;
}

// Sound Management
function playSound(type) {
    // Simple beep sounds using Web Audio API
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    let frequency;
    let duration;
    
    switch(type) {
        case 'start':
            frequency = 800;
            duration = 0.2;
            break;
        case 'end':
            frequency = 600;
            duration = 0.5;
            break;
        case 'tick':
            frequency = 400;
            duration = 0.1;
            break;
        default:
            frequency = 500;
            duration = 0.2;
    }
    
    oscillator.frequency.setValueAtTime(frequency, audioContext.currentTime);
    gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + duration);
    
    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + duration);
}

// Settings Panel Management
function initializeSettingsPanel() {
    const settingsBtn = document.getElementById('settings-btn');
    const settingsModal = document.getElementById('settings-modal');
    const closeBtn = document.getElementById('close-settings');
    
    if (!settingsBtn || !settingsModal || !closeBtn) {
        console.error('Settings panel elements not found');
        return;
    }
    
    settingsBtn.addEventListener('click', openSettings);
    closeBtn.addEventListener('click', closeSettings);
    settingsModal.addEventListener('click', (e) => {
        if (e.target === settingsModal) closeSettings();
    });
    
    // Time buttons
    document.querySelectorAll('.time-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.time-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            settings.focusTime = parseInt(btn.dataset.time);
            if (!isBreak) {
                timerDuration = settings.focusTime * 60;
                timeRemaining = timerDuration;
                updateTimerDisplay();
            }
            saveSettings();
        });
    });
    
    // Break time buttons
    document.querySelectorAll('.break-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.break-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            settings.breakTime = parseInt(btn.dataset.time);
            if (isBreak) {
                timerDuration = settings.breakTime * 60;
                timeRemaining = timerDuration;
                updateTimerDisplay();
            }
            saveSettings();
        });
    });
    
    // Theme buttons
    document.querySelectorAll('.theme-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.theme-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            settings.theme = btn.dataset.theme;
            applyTheme();
            saveSettings();
        });
    });
    
    // Sound toggles
    document.getElementById('start-sound').addEventListener('change', (e) => {
        settings.sounds.start = e.target.checked;
        saveSettings();
    });
    
    document.getElementById('end-sound').addEventListener('change', (e) => {
        settings.sounds.end = e.target.checked;
        saveSettings();
    });
    
    document.getElementById('tick-sound').addEventListener('change', (e) => {
        settings.sounds.tick = e.target.checked;
        saveSettings();
    });
    
    // Update UI to reflect current settings
    updateSettingsUI();
}

function updateSettingsUI() {
    // Update active time buttons
    document.querySelectorAll('.time-btn').forEach(btn => {
        btn.classList.toggle('active', parseInt(btn.dataset.time) === settings.focusTime);
    });
    
    document.querySelectorAll('.break-btn').forEach(btn => {
        btn.classList.toggle('active', parseInt(btn.dataset.time) === settings.breakTime);
    });
    
    document.querySelectorAll('.theme-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.theme === settings.theme);
    });
    
    // Update sound checkboxes
    document.getElementById('start-sound').checked = settings.sounds.start;
    document.getElementById('end-sound').checked = settings.sounds.end;
    document.getElementById('tick-sound').checked = settings.sounds.tick;
}

function openSettings() {
    updateSettingsUI(); // Update UI when opening settings
    document.getElementById('settings-modal').classList.remove('hidden');
}

function closeSettings() {
    document.getElementById('settings-modal').classList.add('hidden');
}
