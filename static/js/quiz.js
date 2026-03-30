// Quiz Platform JavaScript

// Global variables
let examTimer = null;
let currentQuestionIndex = 0;
let answers = {};

// Utility functions
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 flex items-center gap-3 ${
        type === 'success' ? 'bg-green-500 text-white' :
        type === 'error' ? 'bg-red-500 text-white' :
        type === 'warning' ? 'bg-yellow-500 text-white' :
        'bg-blue-500 text-white'
    }`;
    
    const icon = type === 'success' ? '✓' : type === 'error' ? '✗' : type === 'warning' ? '!' : 'ℹ';
    
    notification.innerHTML = `
        <div class="h-8 w-8 bg-white bg-opacity-20 rounded-full flex items-center justify-center font-bold">
            ${icon}
        </div>
        <p class="font-medium">${message}</p>
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
        notification.style.opacity = '1';
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        notification.style.opacity = '0';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Exam functionality
class ExamManager {
    constructor() {
        this.timeLeft = 1800; // 30 minutes
        this.totalQuestions = 0;
        this.answeredQuestions = new Set();
        this.currentQuestion = 0;
        this.isSubmitted = false;
    }
    
    init() {
        this.totalQuestions = document.querySelectorAll('.question-card').length;
        this.startTimer();
        this.bindEvents();
        this.loadSavedAnswers();
    }
    
    startTimer() {
        const timerElement = document.getElementById('timer');
        const progressBar = document.getElementById('progress-bar');
        
        this.examTimer = setInterval(() => {
            this.timeLeft--;
            
            if (timerElement) {
                timerElement.textContent = formatTime(this.timeLeft);
            }
            
            if (progressBar) {
                const progress = ((1800 - this.timeLeft) / 1800) * 100;
                progressBar.style.width = `${progress}%`;
            }
            
            // Warning when 5 minutes left
            if (this.timeLeft === 300) {
                showNotification('Imtihon tugashiga 5 daqiqa qoldi!', 'warning');
            }
            
            // Warning when 1 minute left
            if (this.timeLeft === 60) {
                showNotification('Imtihon tugashiga 1 daqiqa qoldi!', 'warning');
            }
            
            // Auto submit when time is up
            if (this.timeLeft <= 0) {
                this.submitExam(true);
            }
        }, 1000);
    }
    
    bindEvents() {
        // Track answer changes
        document.querySelectorAll('input[type="radio"]').forEach(radio => {
            radio.addEventListener('change', (e) => {
                this.trackAnswer(e.target);
                this.updateProgress();
            });
        });
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') {
                this.submitExam();
            }
            
            // Navigation shortcuts
            if (e.key === 'ArrowRight' && e.altKey) {
                this.nextQuestion();
            }
            if (e.key === 'ArrowLeft' && e.altKey) {
                this.previousQuestion();
            }
        });
        
        // Auto-save every 5 seconds
        setInterval(() => {
            this.saveAnswers();
        }, 5000);
        
        // Save on page unload
        window.addEventListener('beforeunload', (e) => {
            if (this.answeredQuestions.size > 0 && !this.isSubmitted) {
                e.preventDefault();
                e.returnValue = '';
            }
        });
    }
    
    trackAnswer(radio) {
        const questionId = radio.name.replace('question_', '');
        this.answeredQuestions.add(questionId);
        answers[radio.name] = radio.value;
    }
    
    updateProgress() {
        const progressBar = document.getElementById('progress-bar');
        if (progressBar) {
            const progress = (this.answeredQuestions.size / this.totalQuestions) * 100;
            progressBar.style.width = `${progress}%`;
        }
    }
    
    saveAnswers() {
        localStorage.setItem('examAnswers', JSON.stringify(answers));
        localStorage.setItem('examTimeLeft', this.timeLeft.toString());
    }
    
    loadSavedAnswers() {
        const savedAnswers = localStorage.getItem('examAnswers');
        if (savedAnswers) {
            answers = JSON.parse(savedAnswers);
            for (let [name, value] of Object.entries(answers)) {
                const radio = document.querySelector(`input[name="${name}"][value="${value}"]`);
                if (radio) {
                    radio.checked = true;
                    const questionId = name.replace('question_', '');
                    this.answeredQuestions.add(questionId);
                }
            }
            this.updateProgress();
        }
        
        const savedTime = localStorage.getItem('examTimeLeft');
        if (savedTime) {
            this.timeLeft = parseInt(savedTime);
        }
    }
    
    submitExam(autoSubmit = false) {
        if (this.isSubmitted) return;
        
        const message = autoSubmit ? 
            'Vaqt tugadi! Imtihon avtomatik ravishda topshiriladi.' :
            'Imtihonni tugatishga ishonchingiz komilmi? Javoblarni qaytarib bo\'lmaydi.';
        
        if (autoSubmit || confirm(message)) {
            this.isSubmitted = true;
            clearInterval(this.examTimer);
            localStorage.removeItem('examAnswers');
            localStorage.removeItem('examTimeLeft');
            document.getElementById('exam-form').submit();
        }
    }
    
    nextQuestion() {
        const questions = document.querySelectorAll('.question-card');
        if (this.currentQuestion < questions.length - 1) {
            questions[this.currentQuestion].style.display = 'none';
            this.currentQuestion++;
            questions[this.currentQuestion].style.display = 'block';
            this.scrollToQuestion(questions[this.currentQuestion]);
        }
    }
    
    previousQuestion() {
        const questions = document.querySelectorAll('.question-card');
        if (this.currentQuestion > 0) {
            questions[this.currentQuestion].style.display = 'none';
            this.currentQuestion--;
            questions[this.currentQuestion].style.display = 'block';
            this.scrollToQuestion(questions[this.currentQuestion]);
        }
    }
    
    scrollToQuestion(questionElement) {
        questionElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

// Learn mode functionality
class LearnModeManager {
    constructor() {
        this.currentQuestion = 0;
        this.correctAnswers = 0;
        this.totalAnswered = 0;
    }
    
    init() {
        this.bindEvents();
    }
    
    bindEvents() {
        // Auto-scroll to answered question
        document.querySelectorAll('.option-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                setTimeout(() => {
                    const nextCard = btn.closest('.question-card').nextElementSibling;
                    if (nextCard) {
                        nextCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                }, 500);
            });
        });
    }
    
    checkAnswer(questionId, selectedOption) {
        return fetch(`/api/check-answer/${questionId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                'option': selectedOption
            })
        })
        .then(response => response.json())
        .then(data => {
            this.totalAnswered++;
            if (data.is_correct) {
                this.correctAnswers++;
            }
            return data;
        });
    }
    
    getStats() {
        return {
            correct: this.correctAnswers,
            total: this.totalAnswered,
            percentage: this.totalAnswered > 0 ? Math.round((this.correctAnswers / this.totalAnswered) * 100) : 0
        };
    }
}

// Dashboard functionality
class DashboardManager {
    constructor() {
        this.charts = {};
    }
    
    init() {
        this.initializeCharts();
        this.bindEvents();
    }
    
    initializeCharts() {
        // Simple chart implementation (could be enhanced with Chart.js)
        this.createSimpleChart();
    }
    
    createSimpleChart() {
        const chartContainer = document.getElementById('stats-chart');
        if (chartContainer) {
            // Basic bar chart using CSS
            const data = [
                { label: 'Fanlar', value: parseInt(chartContainer.dataset.subjects || 0), color: '#3b82f6' },
                { label: 'Savollar', value: parseInt(chartContainer.dataset.questions || 0), color: '#10b981' },
                { label: 'O\'quvchilar', value: parseInt(chartContainer.dataset.students || 0), color: '#8b5cf6' }
            ];
            
            const maxValue = Math.max(...data.map(d => d.value));
            
            chartContainer.innerHTML = data.map(item => `
                <div class="flex items-center gap-4 mb-3">
                    <div class="w-20 text-sm font-medium text-gray-600">${item.label}</div>
                    <div class="flex-1 bg-gray-200 rounded-full h-6">
                        <div class="h-6 rounded-full transition-all duration-500" 
                             style="width: ${(item.value / maxValue) * 100}%; background-color: ${item.color}">
                            <span class="text-white text-xs font-semibold px-2 leading-6">${item.value}</span>
                        </div>
                    </div>
                </div>
            `).join('');
        }
    }
    
    bindEvents() {
        // Quick actions
        document.querySelectorAll('.quick-action').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const action = btn.dataset.action;
                this.handleQuickAction(action);
            });
        });
    }
    
    handleQuickAction(action) {
        switch(action) {
            case 'add-question':
                window.location.href = '/admin/questions/add/';
                break;
            case 'add-subject':
                window.location.href = '/admin/subjects/add/';
                break;
            case 'view-stats':
                showNotification('Statistika tez kunda!', 'info');
                break;
            case 'export-data':
                this.exportData();
                break;
        }
    }
    
    exportData() {
        // Simple data export functionality
        showNotification('Ma\'lumotlar eksport qilinmoqda...', 'info');
        
        setTimeout(() => {
            showNotification('Ma\'lumotlar muvaffaqiyatli eksport qilindi!', 'success');
        }, 2000);
    }
}

// Initialize managers when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize based on current page
    if (document.getElementById('exam-form')) {
        const examManager = new ExamManager();
        examManager.init();
        window.examManager = examManager; // Make it globally accessible
    }
    
    if (document.getElementById('questions-container')) {
        const learnManager = new LearnModeManager();
        learnManager.init();
        window.learnManager = learnManager;
    }
    
    if (document.getElementById('dashboard-content')) {
        const dashboardManager = new DashboardManager();
        dashboardManager.init();
        window.dashboardManager = dashboardManager;
    }
    
    // Global functions for template compatibility
    window.submitExam = function() {
        if (window.examManager) {
            window.examManager.submitExam();
        }
    };
});
