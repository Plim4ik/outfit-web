document.addEventListener('DOMContentLoaded', () => {
    // Находим все кнопки с классом "heart-btn"
    const heartButtons = document.querySelectorAll('.heart-btn');

    heartButtons.forEach(button => {
        button.addEventListener('click', event => {
            event.preventDefault();

            // Получаем ID образа из атрибута data-outfit-id
            const outfitId = button.getAttribute('data-outfit-id');

            // Отправляем AJAX-запрос
            fetch(`/toggle-favorite/${outfitId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCsrfToken(), // Подставляем CSRF-токен
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    if (data.status === 'added') {
                        // Меняем внешний вид кнопки на "активный" (например, залитое сердце)
                        button.classList.remove('btn-outline-danger');
                        button.classList.add('btn-danger');
                        button.innerHTML = '<i class="bi bi-heart-fill"></i>';
                        alert('Образ добавлен в избранное!');
                    } else if (data.status === 'removed') {
                        // Меняем внешний вид кнопки на "неактивный" (пустое сердце)
                        button.classList.remove('btn-danger');
                        button.classList.add('btn-outline-danger');
                        button.innerHTML = '<i class="bi bi-heart"></i>';
                        alert('Образ удален из избранного!');
                    }
                } else {
                    alert('Что-то пошло не так. Попробуйте снова.');
                }
            })
            .catch(error => {
                console.error('Ошибка:', error);
                alert('Ошибка сети. Попробуйте позже.');
            });
        });
    });

    // Функция для получения CSRF-токена из cookies
    function getCsrfToken() {
        let cookieValue = null;
        const cookies = document.cookie.split(';');
        cookies.forEach(cookie => {
            const trimmedCookie = cookie.trim();
            if (trimmedCookie.startsWith('csrftoken=')) {
                cookieValue = trimmedCookie.substring('csrftoken='.length, trimmedCookie.length);
            }
        });
        return cookieValue;
    }
});
