// Handles AJAX form submissions for NovaTex Factory
document.addEventListener('DOMContentLoaded', function() {
    // Newsletter Form
    const newsletterForm = document.getElementById('newsletter-form');
    if (newsletterForm) {
        newsletterForm.onsubmit = function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            fetch('/subscribe-newsletter/', {
                method: 'POST',
                body: formData,
                headers: { 'X-CSRFToken': formData.get('csrfmiddlewaretoken') }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    document.getElementById('newsletter-content').style.display = 'none';
                    document.getElementById('newsletter-success-block').style.display = 'block';
                } else {
                    alert('Subscription failed. Please check your email address.');
                }
            });
        };
    }

    // Contact Modal Logic
    const contactModal = document.getElementById('contactModal');
    const openBtn = document.getElementById('openContactModal');
    const closeBtn = document.getElementById('closeContactModal');

    if (openBtn) {
        openBtn.onclick = (e) => { e.preventDefault(); contactModal.style.display = 'flex'; };
        closeBtn.onclick = () => { contactModal.style.display = 'none'; };
        window.onclick = (e) => { if (e.target == contactModal) contactModal.style.display = 'none'; };
    }

    // Contact Form AJAX
    const contactForm = document.getElementById('contact-form-modal');
    if (contactForm) {
        contactForm.onsubmit = function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            fetch('/contact-submit/', {
                method: 'POST',
                body: formData,
                headers: { 'X-CSRFToken': formData.get('csrfmiddlewaretoken') }
            })
            .then(response => {
                if (response.ok) {
                    document.getElementById('contact-form-container').style.display = 'none';
                    document.getElementById('form-success-container').style.display = 'block';
                    this.reset();
                }
            });
        };
    }
});