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

/** ----------- Скрипт для сторінки Report --------------- */
document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('chartData');
    if (!container) return;

    const labels = JSON.parse(container.dataset.labels);
    const values = JSON.parse(container.dataset.values);

    // === Chart styles / theme ===
    const chartTheme = {
        fontFamily: 'Segoe UI',
        bar: {
            color: '#e67e22',
            radius: 8,
            thickness: 45
        }
    };

    // === Common font settings ===
    const defaultFont = {
        family: chartTheme.fontFamily,
        size: 13
    };

    // === Chart init ===
    new Chart(document.getElementById('ordersChart'), {
        type: 'bar',
        data: {
            labels,
            datasets: [{
                label: 'Кількість замовлень',
                data: values,
                backgroundColor: chartTheme.bar.color,
                borderRadius: chartTheme.bar.radius,
                barThickness: chartTheme.bar.thickness
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    labels: {
                        font: defaultFont
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        font: { family: chartTheme.fontFamily }
                    }
                },
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1,
                        font: { family: chartTheme.fontFamily }
                    }
                }
            }
        }
    });
});