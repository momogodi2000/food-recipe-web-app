// login.js

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent form submission for demo purposes

        form.classList.add('submitted');
        setTimeout(function() {
            form.submit(); // Uncomment this line to allow form submission
        }, 1000); // Delay form submission for animation
    });
});