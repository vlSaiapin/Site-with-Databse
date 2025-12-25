/**
 * Функція для підтвердження видалення
 * Викликається при натисканні на посилання з класом 'delete-link'
 */
function confirmDelete(event) {
    // Отримуємо назву об'єкта з атрибута data-name (якщо він є)
    const name = event.currentTarget.getAttribute('data-name') || 'цей запис';
    
    // Показуємо діалогове вікно
    const confirmed = confirm(`Ви впевнені, що хочете видалити ${name}?`);
    
    // Якщо користувач натиснув "Скасувати", відміняємо перехід за посиланням
    if (!confirmed) {
        event.preventDefault();
    }
}

// Чекаємо завантаження DOM, щоб призначити обробники
document.addEventListener('DOMContentLoaded', () => {
    // Знаходимо всі посилання для видалення
    const deleteLinks = document.querySelectorAll('.delete-link');
    
    deleteLinks.forEach(link => {
        link.addEventListener('click', confirmDelete);
    });
});

// Додайте це до вашого існуючого document.addEventListener('DOMContentLoaded', ...)
document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.getElementById("sidebar");
    const menuBtn = document.getElementById("menuBtn");
    const closeBtn = document.getElementById("closeBtn");

    // Відкрити меню
    if (menuBtn) {
        menuBtn.onclick = function() {
            sidebar.style.width = "250px";
        };
    }

    // Закрити меню
    if (closeBtn) {
        closeBtn.onclick = function() {
            sidebar.style.width = "0";
        };
    }
});