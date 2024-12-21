document.addEventListener('DOMContentLoaded', function () {
    const toggleButtons = document.querySelectorAll('.toggle-button');
    const progressBar = document.getElementById('progress-bar');
    const itemsToAdd = document.getElementById('items-to-add');
    const recommendationLink = document.getElementById('recommendation-link');
    const maxItems = 10;

    /**
     * Updates the progress bar and remaining items display.
     * @param {number} selectedCount - The number of selected items.
     */
    function updateProgressBar(selectedCount) {
        const remaining = Math.max(0, maxItems - selectedCount);

        // Update progress bar styles and text
        progressBar.style.width = `${(selectedCount / maxItems) * 100}%`;
        progressBar.setAttribute('aria-valuenow', selectedCount);
        progressBar.textContent = `${selectedCount}/${maxItems}`;
        itemsToAdd.textContent = remaining;

        // Enable or disable the recommendation link
        recommendationLink.classList.toggle('disabled', remaining > 0);
    }

    /**
     * Updates the toggle button's text and style based on selection status.
     * @param {HTMLElement} button - The button element.
     * @param {boolean} isSelected - Whether the item is selected.
     */
    function updateButtonState(button, isSelected) {
        button.textContent = isSelected ? 'Убрать' : 'Добавить';
        button.classList.toggle('btn-success', isSelected);
        button.classList.toggle('btn-success-outline', !isSelected);
    }

    /**
     * Handles the toggle button click event.
     * @param {Event} event - The click event.
     */
    function handleToggleClick(event) {
        event.preventDefault();

        const button = event.target;
        const itemId = button.dataset.itemId;
        const card = button.closest('.item-card');

        fetch(`/toggle_item/${itemId}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data && typeof data.selected_count === 'number') {
                    // Update UI based on the response
                    card.classList.toggle('selected', data.selected);
                    updateButtonState(button, data.selected);
                    updateProgressBar(data.selected_count);
                } else {
                    console.error('Invalid data received from server:', data);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    // Attach event listeners to all toggle buttons
    toggleButtons.forEach(button => {
        button.addEventListener('click', handleToggleClick);

        // Initialize button state
        const card = button.closest('.item-card');
        const isSelected = card.classList.contains('selected');
        updateButtonState(button, isSelected);
    });

    // Initialize progress bar with current selected items count
    const selectedItemsCount = document.querySelectorAll('.item-card.selected').length;
    updateProgressBar(selectedItemsCount);
});
