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

  if (!burgerMenu || !overlay) {
    console.warn("Burger menu or overlay not found in DOM.");
    return;
  }

  burgerMenu.addEventListener('click', function() {
    // NOTE: CSS expects .open on #burger-menu and .show on #menu
    this.classList.toggle('open');
    overlay.classList.toggle('show');

    // optional: prevent body scroll while menu is open
    document.body.classList.toggle('menu-open');
  });

});
