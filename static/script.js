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

    // === Universal Burger Menu Implementation ===
    const burgerMenu = document.getElementById('burger-menu');
    const menuOverlay = document.getElementById('menu');
    const backdrop = document.getElementById('menu-backdrop');
    let focusableElements;
    let firstFocusableElement;
    let lastFocusableElement;

    if (!burgerMenu || !menuOverlay || !backdrop) {
        console.warn("Burger menu, overlay, or backdrop not found in DOM.");
        return;
    }

    // Get all focusable elements in the menu for keyboard navigation
    function setFocusableElements() {
        focusableElements = menuOverlay.querySelectorAll(
            'a[href], button, textarea, input[type="text"], input[type="radio"], input[type="checkbox"], select'
        );
        firstFocusableElement = focusableElements[0];
        lastFocusableElement = focusableElements[focusableElements.length - 1];
    }
    
    function openMenu() {
        // Update ARIA states
        burgerMenu.setAttribute('aria-expanded', 'true');
        menuOverlay.setAttribute('aria-hidden', 'false');
        
        // Show menu and backdrop with animation classes
        burgerMenu.classList.add('open');
        menuOverlay.classList.add('show');
        backdrop.classList.add('show');
        
        // Prevent scrolling
        document.body.classList.add('menu-open');
        
        // Set focus trap
        setFocusableElements();
        
        // Set focus to the menu after a short delay to allow animation
        setTimeout(() => {
            menuOverlay.focus();
        }, 100);
    }

    function closeMenu() {
        // Update ARIA states
        burgerMenu.setAttribute('aria-expanded', 'false');
        menuOverlay.setAttribute('aria-hidden', 'true');
        
        // Hide menu and backdrop
        burgerMenu.classList.remove('open');
        menuOverlay.classList.remove('show');
        backdrop.classList.remove('show');
        
        // Re-enable scrolling
        document.body.classList.remove('menu-open');
        
        // Return focus to burger button
        burgerMenu.focus();
    }

    // Toggle menu when clicking burger icon
    burgerMenu.addEventListener('click', function() {
        if (menuOverlay.classList.contains('show')) {
            closeMenu();
        } else {
            openMenu();
        }
    });

    // Close menu when clicking on backdrop
    backdrop.addEventListener('click', closeMenu);
    
    // Close menu on Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && menuOverlay.classList.contains('show')) {
            closeMenu();
        }
        
        // Trap focus inside modal when open
        if (e.key === 'Tab' && menuOverlay.classList.contains('show')) {
            // If shift + tab and on first element, go to last element
            if (e.shiftKey && document.activeElement === firstFocusableElement) {
                e.preventDefault();
                lastFocusableElement.focus();
            } 
            // If tab and on last element, cycle back to first element
            else if (!e.shiftKey && document.activeElement === lastFocusableElement) {
                e.preventDefault();
                firstFocusableElement.focus();
            }
        }
    });
    
    // Handle window resize to ensure menu works at all screen sizes
    window.addEventListener('resize', function() {
        if (menuOverlay.classList.contains('show')) {
            setFocusableElements(); // Update focusable elements on resize
        }
    });
});
