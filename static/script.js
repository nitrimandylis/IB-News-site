        // Hamburger menu toggle
        const hamburger = document.querySelector('.hamburger');
        const navWrapper = document.querySelector('.nav-wrapper');

        hamburger?.addEventListener('click', () => {
            const isExpanded = hamburger.getAttribute('aria-expanded') === 'true';
            hamburger.setAttribute('aria-expanded', !isExpanded);
            navWrapper.classList.toggle('nav-open');
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

                        const articleLink = card.querySelector('a');

                        if(articleLink) {

                            articleLink.click();

                        }

                    });

                    card.addEventListener('keypress', (e) => {

                        if (e.key === 'Enter' || e.key === ' ') {

                            const articleLink = card.querySelector('a');

                            if(articleLink) {

                                articleLink.click();

                            }

                        }

                    });

                });

        

        function toggleTag(element) {

            element.classList.toggle('active');

            updateSelectedTagsInput();

        }

        

        function updateSelectedTagsInput() {

            const activeTags = Array.from(document.querySelectorAll('.tag-chip.active'))

                .map(chip => chip.textContent);

            const selectedTagsInput = document.getElementById('selected-tags-input');

            if (selectedTagsInput) {

                selectedTagsInput.value = activeTags.join(',');

            }

        }

        