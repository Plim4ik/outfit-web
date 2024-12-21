document.addEventListener('DOMContentLoaded', function () {
    const progressBar = document.getElementById('progress-bar');
    const itemsToAdd = document.getElementById('items-to-add');
    const recommendationLink = document.getElementById('recommendation-link');
    const cards = document.querySelectorAll('.item-card');

    function updateProgressBar(selectedCount) {
        const maxItems = 10;
        const progress = (selectedCount / maxItems) * 100;
        progressBar.style.width = `${progress}%`;
        progressBar.setAttribute('aria-valuenow', selectedCount);
        progressBar.textContent = `${selectedCount}/${maxItems}`;

        const remaining = maxItems - selectedCount;
        itemsToAdd.textContent = remaining > 0 ? remaining : 0;
        recommendationLink.style.display = remaining <= 0 ? 'block' : 'none';
    }

    function toggleItem(card) {
        const itemId = card.dataset.itemId;
        fetch(`/toggle_item/${itemId}/`)
            .then(response => {
                if (!response.ok) throw new Error('Ошибка сети');
                return response.json();
            })
            .then(data => {
                if (data && typeof data.selected_count === 'number') {
                    const icon = card.querySelector('.icon-overlay i');

                    if (data.selected) {
                        // Товар добавлен: заменить плюсик на галочку
                        icon.className = 'bi bi-check-circle-fill text-success';
                    } else {
                        // Товар убран: вернуть плюсик
                        icon.className = 'bi bi-plus-circle-fill text-secondary';
                    }

                    updateProgressBar(data.selected_count);
                }
            })
            .catch(error => console.error('Ошибка:', error));
    }

    cards.forEach(card => {
        card.addEventListener('click', function () {
            toggleItem(card);
        });
    });

    // Инициализация прогресса при загрузке страницы
    updateProgressBar(parseInt(progressBar.getAttribute('aria-valuenow')));
});
