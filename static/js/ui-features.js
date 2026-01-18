// Handles scroll-to-top and Age Verification Modal
document.addEventListener('DOMContentLoaded', function() {
    // Scroll to Top logic
    const scrollBtn = document.getElementById('scrollToTopBtn');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 300) {
            scrollBtn.classList.add('visible');
        } else {
            scrollBtn.classList.remove('visible');
        }
    });

    scrollBtn.addEventListener('click', (e) => {
        e.preventDefault();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // Age Verification Logic
    const ageModal = document.getElementById('ageModal');
    if (ageModal) {
        const btnYes = document.getElementById('btnAgeYes');
        if (localStorage.getItem('ageVerified') === 'true') {
            ageModal.style.display = 'none';
        } else {
            ageModal.style.display = 'flex';
        }

        btnYes.addEventListener('click', function() {
            localStorage.setItem('ageVerified', 'true');
            ageModal.classList.add('hidden');
            setTimeout(() => { ageModal.style.display = 'none'; }, 500);
        });
    }
});

const header = document.querySelector('.site-header');

window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        header.classList.add('header-scrolled');
    } else {
        header.classList.remove('header-scrolled');
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // Select the "Contact" link in the main navigation
    const navContactLink = document.querySelector('.nav-links a[href="/#contact"]');
    const contactModal = document.getElementById('contactModal');

    if (navContactLink && contactModal) {
        navContactLink.addEventListener('click', function(e) {
            e.preventDefault(); // Stop page scroll
            contactModal.style.display = 'flex'; // Open modal immediately
        });
    }
});