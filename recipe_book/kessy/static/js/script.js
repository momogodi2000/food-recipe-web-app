// scripts.js

document.addEventListener('DOMContentLoaded', function () {
    const elements = document.querySelectorAll('.fade-in');
    elements.forEach(element => {
        element.classList.add('visible');
    });
});
