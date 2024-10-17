$(document).ready(function() {
    $('#attendance-form').on('submit', function(event) {
        event.preventDefault(); // Prevent form from submitting normally

        $.ajax({
            type: 'POST',
            url: '{% url "record_attendance" %}', // Ensure the URL is correct
            data: $(this).serialize(), // Serialize form data
            success: function(response) {
                if (response.status === 'success') {
                    toastr.success(response.message); // Show success message
                } else {
                    toastr.error(response.message); // Show error message
                }
            },
            error: function(xhr, status, error) {
                toastr.error('An error occurred. Please try again.');
            }
        });
    });
});