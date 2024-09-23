document.addEventListener('DOMContentLoaded', function () {
    // Handle Add Data
    const addForm = document.getElementById('add-form');
    addForm.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the default form submission

        const formData = new FormData(addForm);
        fetch('', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Refresh the page or update the UI dynamically
                alert(data.message);
                location.reload(); // Reloads the page to see the new data
            } else {
                alert(data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    });

    // Handle Update Data
    const updateForm = document.getElementById('update-data-form');
    if (updateForm) {
        updateForm.addEventListener('submit', function (event) {
            event.preventDefault();

            const formData = new FormData(updateForm);
            fetch('', {
                method: 'POST',
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(data.message);
                    location.reload(); // Reloads the page to see updated data
                } else {
                    alert(data.message);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }

    // Handle Delete Data
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function () {
            const metricToDelete = this.dataset.metric;

            if (confirm(`Are you sure you want to delete ${metricToDelete}?`)) {
                const formData = new FormData();
                formData.append('action', 'delete');
                formData.append('year', document.getElementById('year-select').value);
                formData.append('month', document.getElementById('month-select').value);
                formData.append('metric_to_delete', metricToDelete);

                fetch('', {
                    method: 'POST',
                    body: formData,
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert(data.message);
                        location.reload(); // Reloads the page to see updated data
                    } else {
                        alert(data.message);
                    }
                })
                .catch(error => console.error('Error:', error));
            }
        });
    });

    // Show update form
    const updateButtons = document.querySelectorAll('.btn-update');
    updateButtons.forEach(button => {
        button.addEventListener('click', function () {
            const metricToUpdate = this.dataset.metric;
            document.getElementById('update-metric-old-name').value = metricToUpdate;
            document.getElementById('update-form').style.display = 'block';
        });
    });
});
