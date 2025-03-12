document.addEventListener('DOMContentLoaded', () => {
    const userInfoForm = document.getElementById('user-info-form');
    const toast = document.getElementById('toast');

    const user = JSON.parse(localStorage.getItem('user'));
    if (!user) {
        window.location.href = 'index.html';
    }

    userInfoForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const formData = new FormData(userInfoForm);
        const userData = Object.fromEntries(formData.entries());

        const combinedUserData = { ...user, ...userData };
 
        localStorage.setItem('userData', JSON.stringify(combinedUserData));

        showToast('Генерация рекомендаций...');
        setTimeout(() => {
            window.location.href = 'recommendations.html';
        }, 1500);
    });

    function showToast(message) {
        toast.textContent = message;
        toast.classList.add('show');
        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }
});
