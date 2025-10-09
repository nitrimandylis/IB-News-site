// Function to update the scroll progress bar
function updateProgressBar() {
  const { scrollTop, scrollHeight, clientHeight } = document.documentElement;

  // Calculate the scroll percentage
  const scrollPercent = (scrollTop / (scrollHeight - clientHeight)) * 100;

  // Update the width of the progress bar
  const progressBar = document.getElementById('progressBar');
  if (progressBar) {
    progressBar.style.width = `${scrollPercent}%`;
  }
}

// Add event listener for scroll events
document.addEventListener('scroll', updateProgressBar);

var burgerMenu = document.getElementById('burger-menu');

var overlay = document.getElementById('menu');

burgerMenu.addEventListener('click', function() {
  this.classList.toggle("close");
  overlay.classList.toggle("overlay");
});

