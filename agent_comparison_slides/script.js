document.addEventListener('DOMContentLoaded', () => {
    const slides = document.querySelector('.slides');
    const sections = document.querySelectorAll('section');
    const totalSlides = sections.length;
    let currentSlide = 0;

    function goToSlide(slideIndex) {
        if (slideIndex < 0 || slideIndex >= totalSlides) return;
        currentSlide = slideIndex;
        slides.style.transform = `translateX(-${currentSlide * 100}vw)`;
        updateNavButtons();
    }

    function createNav() {
        const nav = document.createElement('div');
        nav.className = 'nav';

        const prevButton = document.createElement('button');
        prevButton.id = 'prev';
        prevButton.textContent = '上一頁';
        prevButton.addEventListener('click', () => goToSlide(currentSlide - 1));

        const nextButton = document.createElement('button');
        nextButton.id = 'next';
        nextButton.textContent = '下一頁';
        nextButton.addEventListener('click', () => goToSlide(currentSlide + 1));

        nav.appendChild(prevButton);
        nav.appendChild(nextButton);
        document.body.appendChild(nav);
    }

    function updateNavButtons() {
        const prevButton = document.getElementById('prev');
        const nextButton = document.getElementById('next');
        if (!prevButton || !nextButton) return;

        prevButton.disabled = currentSlide === 0;
        nextButton.disabled = currentSlide === totalSlides - 1;
    }

    createNav();
    goToSlide(0);

    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowRight') {
            goToSlide(currentSlide + 1);
        }
        if (e.key === 'ArrowLeft') {
            goToSlide(currentSlide - 1);
        }
    });
});
