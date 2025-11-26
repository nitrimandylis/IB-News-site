// Hamburger menu toggle
        const hamburger = document.querySelector('.hamburger');
        const nav = document.querySelector('nav');

        hamburger?.addEventListener('click', () => {
            hamburger.setAttribute('aria-expanded', 
                hamburger.getAttribute('aria-expanded') === 'false' ? 'true' : 'false'
            );
        });

        // Section navigation active state
        const sectionLinks = document.querySelectorAll('.section-nav a');
        sectionLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                sectionLinks.forEach(l => l.classList.remove('active'));
                link.classList.add('active');
            });
        });

        // Article card click handler
        const articleCards = document.querySelectorAll('.article-card');
        articleCards.forEach(card => {
            card.addEventListener('click', () => {
                console.log('Article clicked - navigate to detail view');
            });
            card.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    console.log('Article activated via keyboard');
                }
            });
        });