document.addEventListener('DOMContentLoaded', function () {
    const stars = document.querySelectorAll('.rating .star');

    stars.forEach(star => {
        star.addEventListener('click', () => {
            stars.forEach(s => s.classList.remove('selected'));
            star.classList.add('selected');
            const ratingValue = star.getAttribute('data-value');
            console.log(`Rated: ${ratingValue}`);
        });

        star.addEventListener('mouseover', () => {
            stars.forEach(s => s.classList.remove('hover'));
            star.classList.add('hover');
            star.previousElementSibling?.classList.add('hover');
        });

        star.addEventListener('mouseout', () => {
            stars.forEach(s => s.classList.remove('hover'));
        });
    });
});
