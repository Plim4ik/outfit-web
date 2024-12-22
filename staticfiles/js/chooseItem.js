document.addEventListener('DOMContentLoaded', function () {
    const itemsToAdd = document.getElementById('items-to-add');
    const recommendationLink = document.getElementById('recommendation-link');
    const cards = document.querySelectorAll('.item-card');


    // Функция переключения состояния товара
    function toggleItem(card) {
        const itemId = card.dataset.itemId;
        const icon = card.querySelector('.icon-overlay i');

        // Мгновенное изменение иконки (плюс/галочка)
        if (icon.classList.contains('bi-plus-circle-fill')) {
            icon.className = 'bi bi-check-circle-fill text-success'; // Товар добавлен
        } else {
            icon.className = 'bi bi-plus-circle-fill text-secondary'; // Товар убран
        }

        // Отправка запроса на сервер для обновления состояния
        fetch(`/toggle_item/${itemId}/`)
            .then(response => {
                if (!response.ok) throw new Error('Ошибка сети');
                return response.json();
            })
            .then(data => {
                if (data && typeof data.selected_count === 'number') {
                    updateProgressBar(data.selected_count); // Обновление прогресса с сервера
                }
            })
            .catch(error => console.error('Ошибка:', error));
    }

    // Добавляем слушателя событий для всех карточек товаров
    cards.forEach(card => {
        card.addEventListener('click', function () {
            toggleItem(card);
        });
    });
});
