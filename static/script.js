document.addEventListener("DOMContentLoaded", function() {
    // Scroll progress bar
    function updateProgressBar() {
        const { scrollTop, scrollHeight, clientHeight } = document.documentElement;
        const scrollPercent = (scrollTop / (scrollHeight - clientHeight)) * 100;
        const progressBar = document.getElementById('progressBar');
        if (progressBar) progressBar.style.width = `${scrollPercent}%`;
    }
    document.addEventListener('scroll', updateProgressBar);

    // Burger menu toggle
    const burgerMenu = document.getElementById('burger-menu');
    const overlay = document.getElementById('menu');

    burgerMenu.addEventListener('click', function() {
        this.classList.toggle("close");
        overlay.classList.toggle("overlay");
    });
});
