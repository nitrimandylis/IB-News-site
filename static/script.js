// Wait until the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function() {

  // === Scroll Progress Bar ===
  function updateProgressBar() {
    const { scrollTop, scrollHeight, clientHeight } = document.documentElement;
    const scrollPercent = (scrollTop / (scrollHeight - clientHeight)) * 100;

    const progressBar = document.getElementById('progressBar');
    if (progressBar) {
      progressBar.style.width = `${scrollPercent}%`;
    }
  }

  document.addEventListener('scroll', updateProgressBar);

  // === Burger Menu Toggle ===
  const burgerMenu = document.getElementById('burger-menu');
  const overlay = document.getElementById('menu');

  if (burgerMenu && overlay) {
    burgerMenu.addEventListener('click', function() {
      // Toggle classes
      this.classList.toggle("close");
      overlay.classList.toggle("overlay");
    });
  } else {
    console.warn("Burger menu or overlay not found!");
  }

});
