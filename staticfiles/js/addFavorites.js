document.addEventListener('DOMContentLoaded', () => {
    // Находим все кнопки с классом "heart-btn"
    const heartButtons = document.querySelectorAll('.heart-btn');

    heartButtons.forEach(button => {
        button.addEventListener('click', event => {
            event.preventDefault();

            // Получаем ID образа из атрибута data-outfit-id
            const outfitId = button.getAttribute('data-outfit-id');

            // Отправляем AJAX-запрос
            fetch(`/add-to-favorites/${outfitId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCsrfToken(), // Подставляем CSRF-токен
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Меняем внешний вид кнопки на "активный" (например, залитое сердце)
                    button.classList.remove('btn-outline-danger');
                    button.classList.add('btn-danger');
                    button.innerHTML = '<i class="bi bi-heart-fill"></i>';

                    // Показываем уведомление об успешном добавлении
                    alert('Образ добавлен в избранное!');
                } else if (data.info) {
                    // Показываем сообщение, если образ уже в избранном
                    alert(data.info);
                } else {
                    // В случае ошибки
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
