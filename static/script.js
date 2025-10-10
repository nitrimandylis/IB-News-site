// Wait until the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function() {

    // === Scroll Progress Bar ===
    function updateProgressBar() {
        const { scrollTop, scrollHeight, clientHeight } = document.documentElement;
        const scrollPercent = (scrollTop / (scrollHeight - clientHeight)) * 100;
        const progressBar = document.getElementById('progressBar');
        if (progressBar) progressBar.style.width = `${scrollPercent}%`;
    }

    document.addEventListener('scroll', updateProgressBar);

    // === Burger Menu Toggle ===
    const burgerMenu = document.getElementById('burger-menu');
    const overlay = document.getElementById('menu');
    const backdrop = document.getElementById('menu-backdrop');

    if (!burgerMenu || !overlay || !backdrop) {
        console.warn("Burger menu, overlay, or backdrop not found in DOM.");
        return;
    }

    function openMenu() {
        burgerMenu.classList.add('open');
        overlay.classList.add('show');
        backdrop.classList.add('show');          // show backdrop
        document.body.classList.add('menu-open'); // optional: prevent scrolling
    }

    function closeMenu() {
        burgerMenu.classList.remove('open');
        overlay.classList.remove('show');
        backdrop.classList.remove('show');       // hide backdrop
        document.body.classList.remove('menu-open');
    }

    // Toggle menu when clicking burger icon
    burgerMenu.addEventListener('click', function() {
        if (overlay.classList.contains('show')) {
            closeMenu();
        } else {
            openMenu();
        }
    });

    // Close menu when clicking on backdrop
    backdrop.addEventListener('click', closeMenu);

});
