// Timer logic for Pomodoro Timer
let timerDuration = 25 * 60; // 25 minutes in seconds
let timeRemaining = timerDuration;
let timerInterval = null;
let particleSystem = null;

// Particle system for background effects
class ParticleSystem {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.particles = [];
        this.animationId = null;
        this.isActive = false;
        
        // Setup canvas size
        this.resizeCanvas();
        window.addEventListener('resize', () => this.resizeCanvas());
    }
    
    resizeCanvas() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }
    
    createParticle() {
        return {
            x: Math.random() * this.canvas.width,
            y: Math.random() * this.canvas.height,
            vx: (Math.random() - 0.5) * 0.5,
            vy: (Math.random() - 0.5) * 0.5,
            size: Math.random() * 3 + 1,
            opacity: Math.random() * 0.3 + 0.1,
            life: Math.random() * 200 + 100
        };
    }
    
    start() {
        if (this.isActive) return;
        this.isActive = true;
        this.particles = [];
        
        // Create initial particles
        for (let i = 0; i < 30; i++) {
            this.particles.push(this.createParticle());
        }
        
        this.animate();
    }
    
    stop() {
        this.isActive = false;
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
            this.animationId = null;
        }
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    }
    
    animate() {
        if (!this.isActive) return;
        
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Update and draw particles
        for (let i = this.particles.length - 1; i >= 0; i--) {
            const particle = this.particles[i];
            
            particle.x += particle.vx;
            particle.y += particle.vy;
            particle.life--;
            
            // Wrap around screen edges
            if (particle.x < 0) particle.x = this.canvas.width;
            if (particle.x > this.canvas.width) particle.x = 0;
            if (particle.y < 0) particle.y = this.canvas.height;
            if (particle.y > this.canvas.height) particle.y = 0;
            
            // Remove dead particles
            if (particle.life <= 0) {
                this.particles.splice(i, 1);
                continue;
            }
            
            // Draw particle
            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
            this.ctx.fillStyle = `rgba(123, 110, 246, ${particle.opacity})`;
            this.ctx.fill();
        }
        
        // Add new particles occasionally
        if (Math.random() < 0.02 && this.particles.length < 50) {
            this.particles.push(this.createParticle());
        }
        
        this.animationId = requestAnimationFrame(() => this.animate());
    }
}

// Ripple effect for timer start
function createRippleEffect() {
    const timerSection = document.querySelector('.timer-section');
    const ripple = document.createElement('div');
    ripple.className = 'ripple-effect';
    timerSection.appendChild(ripple);
    
    // Remove ripple after animation
    setTimeout(() => {
        if (ripple.parentNode) {
            ripple.parentNode.removeChild(ripple);
        }
    }, 1000);
}

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
    
    // Add active class for visual feedback
    document.querySelector('.timer-section').classList.add('active');
    
    // Start visual effects
    createRippleEffect();
    if (particleSystem) {
        particleSystem.start();
    }
    
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
    
    // Remove active class
    document.querySelector('.timer-section').classList.remove('active');
    
    // Stop visual effects
    if (particleSystem) {
        particleSystem.stop();
    }
    
    updateTimerDisplay();
}

function handleSessionComplete() {
    // Remove active class
    document.querySelector('.timer-section').classList.remove('active');
    
    // Stop visual effects
    if (particleSystem) {
        particleSystem.stop();
    }
    
    // TODO: Notify backend, update progress, show notification
    alert('Session Complete!');
}

function updateProgressBar() {
    const percent = (timerDuration - timeRemaining) / timerDuration;
    const circle = document.getElementById('progress-circle');
    const radius = circle.r.baseVal.value;
    const circumference = 2 * Math.PI * radius;
    
    // Update progress arc
    circle.style.strokeDasharray = `${circumference}`;
    circle.style.strokeDashoffset = `${circumference * (1 - percent)}`;
    
    // Dynamic color transition based on remaining time percentage
    const remainingPercent = timeRemaining / timerDuration;
    let color;
    
    if (remainingPercent > 0.66) {
        // Blue phase (100%-66% remaining): Cool start phase
        const blueIntensity = (remainingPercent - 0.66) / 0.34;
        color = `hsl(${235 + blueIntensity * 10}, 70%, ${60 + blueIntensity * 10}%)`;
    } else if (remainingPercent > 0.33) {
        // Yellow phase (66%-33% remaining): Warning phase
        const transition = (remainingPercent - 0.33) / 0.33;
        const hue = 235 + (60 - 235) * (1 - transition); // Blue to Yellow
        color = `hsl(${hue}, 70%, 65%)`;
    } else {
        // Red phase (33%-0% remaining): Critical focus phase
        const redIntensity = (0.33 - remainingPercent) / 0.33;
        color = `hsl(${15 - redIntensity * 15}, ${70 + redIntensity * 20}%, ${50 + redIntensity * 15}%)`;
    }
    
    circle.style.stroke = color;
    
    // Add smooth transition
    circle.style.transition = 'stroke 0.5s ease-in-out';
}

document.getElementById('start-btn').addEventListener('click', startTimer);
document.getElementById('reset-btn').addEventListener('click', resetTimer);

document.addEventListener('DOMContentLoaded', () => {
    // Initialize particle system
    const canvas = document.createElement('canvas');
    canvas.id = 'particle-canvas';
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    canvas.style.pointerEvents = 'none';
    canvas.style.zIndex = '-1';
    document.body.appendChild(canvas);
    
    particleSystem = new ParticleSystem(canvas);
    
    updateTimerDisplay();
});
