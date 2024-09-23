document.addEventListener('DOMContentLoaded', () => {
    // Theme toggle functionality
    const toggleButton = document.getElementById('toggle-mode');
    const body = document.body;

    // Load mode from local storage
    const currentMode = localStorage.getItem('mode') || 'dark';
    if (currentMode === 'light') {
        body.classList.add('light-mode');
        toggleButton.innerHTML = '<i class="fas fa-sun"></i>';
    }

    toggleButton.addEventListener('click', () => {
        body.classList.toggle('light-mode');
        const newMode = body.classList.contains('light-mode') ? 'light' : 'dark';
        localStorage.setItem('mode', newMode);
        toggleButton.innerHTML = newMode === 'light' ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';

        // Add transition effect for background color
        body.style.transition = 'background-color 0.5s ease';
    });

    // CRUD operations functionality
    const addForm = document.getElementById('add-form');
    const updateForm = document.getElementById('update-form');
    const updateButtons = document.querySelectorAll('.btn-update');
    const deleteButtons = document.querySelectorAll('.btn-delete');

    addForm.addEventListener('submit', function(e) {
        e.preventDefault();
        submitForm(this);
    });

    updateButtons.forEach(button => {
        button.addEventListener('click', function() {
            const metric = this.getAttribute('data-metric');
            const value = this.getAttribute('data-value');
            document.getElementById('update-metric-old-name').value = metric; // Set old metric name
            document.getElementById('update-metric-new-name').value = metric; // Set new metric name to old one as default
            document.getElementById('update-metric-value').value = value; // Set current value
            updateForm.style.display = 'block'; // Show update form
        });
    });

    updateForm.querySelector('form').addEventListener('submit', function(e) {
        e.preventDefault();
        submitForm(this); // Submit the update form
    });

    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const metric = this.getAttribute('data-metric');
            if (confirm(`Are you sure you want to delete the metric "${metric}"?`)) {
                const form = new FormData();
                form.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);
                form.append('action', 'delete');
                form.append('year', document.querySelector('[name=year]').value);
                form.append('month', document.querySelector('[name=month]').value);
                form.append('metric_to_delete', metric);
                submitForm(form);
            }
        });
    });

    function submitForm(form) {
        fetch('', {
            method: 'POST',
            body: form instanceof FormData ? form : new FormData(form),
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            if (data.success) {
                location.reload(); // Reload the page to show updated data
            }
        })
        .catch(error => console.error('Error:', error));
    }
});
