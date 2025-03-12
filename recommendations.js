document.addEventListener('DOMContentLoaded', () => {
    const tabs = document.querySelectorAll('.tab');
    const tabContents = document.querySelectorAll('.tab-content');
    const progressBar = document.getElementById('progress-bar');
    const progressText = document.getElementById('progress-text');
    const logoutButton = document.getElementById('logout');
    const toast = document.getElementById('toast');

    const userData = JSON.parse(localStorage.getItem('userData'));
    if (!userData) {
        window.location.href = 'index.html';
    }

    const dietRecommendations = [
        { title: 'Завтрак', description: 'Овсянка с ягодами и орехами' },
        { title: 'Обед', description: 'Салат с курицей на гриле и овощами' },
        { title: 'Ужин', description: 'Запечённый лосось с киноа и брокколи на пару' },
        { title: 'Перекус', description: 'Греческий йогурт с мёдом и миндалем' },
    ];

    const exerciseRecommendations = [
        { title: 'Кардио', description: '30 минут бега или езды на велосипеде' },
        { title: 'Силовые упражнения', description: '3 подхода по 10 повторений: приседания, отжимания и выпады' },
        { title: 'Гибкость', description: '15 минут йоги или растяжки' },
        { title: 'Кор', description: '3 подхода по 20 повторений: планка, скручивания и скручивания с поворотами' },
    ];

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const tabId = tab.getAttribute('data-tab');
            tabs.forEach(t => t.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            tab.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        });
    });

    function renderRecommendations(recommendations, containerId) {
        const container = document.getElementById(containerId);
        container.innerHTML = recommendations.map(item => `
            <div class="recommendation-card">
                <h4>${item.title}</h4>
                <p>${item.description}</p>
                <button class="complete-btn" data-item="${item.title}">Выполнено</button>
            </div>
        `).join('');
    }

    renderRecommendations(dietRecommendations, 'diet-recommendations');
    renderRecommendations(exerciseRecommendations, 'exercise-recommendations');

    let completedTasks = 0;
    const totalTasks = dietRecommendations.length + exerciseRecommendations.length;

    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('complete-btn')) {
            e.target.classList.toggle('completed');
            if (e.target.classList.contains('completed')) {
                completedTasks++;
                e.target.textContent = 'Завершено';
            } else {
                completedTasks--;
                e.target.textContent = 'Выполнено';
            }
            updateProgress();
        }
    });

    function updateProgress() {
        const percentage = (completedTasks / totalTasks) * 100;
        progressBar.style.width = `${percentage}%`;
        progressText.textContent = `${completedTasks} из ${totalTasks} задач выполнено`;
    }

    logoutButton.addEventListener('click', (e) => {
        e.preventDefault();
        localStorage.removeItem('user');
        localStorage.removeItem('userData');
        window.location.href = 'index.html';
    });

    function showToast(message) {
        toast.textContent = message;
        toast.classList.add('show');
        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }

    showToast(`Добро пожаловать, ${userData.name}! Вот ваши персональные рекомендации.`);
});
