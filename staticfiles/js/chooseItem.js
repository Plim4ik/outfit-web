document.addEventListener('DOMContentLoaded', function() {
    const toggleButtons = document.querySelectorAll('.toggle-button');
    const progressBar = document.getElementById('progress-bar');
    const itemsToAdd = document.getElementById('items-to-add');
    const recommendationLink = document.getElementById('recommendation-link');
    
    function updateProgressBar(selectedCount) {
        const maxItems = 10;
        // Ensure selectedCount is a number and not NaN
        const remaining = Math.max(0, maxItems - (Number(selectedCount) || 0));

        progressBar.style.width = `${(remaining / maxItems) * 100}%`;
        progressBar.setAttribute('aria-valuenow', remaining);
        progressBar.textContent = `${maxItems - remaining}/${maxItems}`;
        itemsToAdd.textContent = remaining;

        // Enable recommendation link if selected count is equal to max items
        if (remaining === 0) {
            recommendationLink.classList.remove('disabled');
        } else {
            recommendationLink.classList.add('disabled');
        }
    }

    toggleButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();

            const itemId = this.dataset.itemId;
            const card = this.closest('.item-card');
            const buttonText = this;

            fetch(`/toggle_item/${itemId}/`)
                .then(response => {
                    if (!response.ok) {
                        console.error('Error fetching:', response.statusText);
                        throw new Error("Network response was not ok.");
                    }
                    return response.json();
                })
                .then(data => {
                    card.classList.toggle('selected', data.selected);
                    buttonText.textContent = data.selected ? 'Убрать' : 'Добавить';

                    // Update progress bar and remaining count
                    updateProgressBar(data.selected_count);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        });
    });

    // Initialize progress bar with current selected count
    const selectedItemsCount = document.querySelectorAll('.item-card.selected').length;
    updateProgressBar(selectedItemsCount);
});
