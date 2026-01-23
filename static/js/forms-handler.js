// Handles AJAX form submissions & Modal Logic for NovaTex Factory
document.addEventListener('DOMContentLoaded', function() {

    // 1. Newsletter Form
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

    // 2. Contact Modal Logic
    const contactModal = document.getElementById('contactModal');
    const closeBtn = document.getElementById('closeContactModal');
    
    // Элементы внутри модального окна (Форма и Блок успеха)
    const formContainer = document.getElementById('contact-form-container');
    const successContainer = document.getElementById('form-success-container');

    // А. Логика ОТКРЫТИЯ (с автоматическим сбросом)
    const openTriggers = document.querySelectorAll('.contact-cta-btn, #openContactModal, a[href="/contact"]');

    if (contactModal) {
        openTriggers.forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.preventDefault(); 
                
                // === ВАЖНЫЙ FIX: СБРОС СОСТОЯНИЯ ===
                // При каждом открытии принудительно показываем форму и прячем "Спасибо"
                if (formContainer) formContainer.style.display = 'block';
                if (successContainer) successContainer.style.display = 'none';
                // ===================================

                contactModal.style.display = 'flex'; 
            });
        });

        // Б. Логика ЗАКРЫТИЯ
        if (closeBtn) {
            closeBtn.onclick = () => { 
                contactModal.style.display = 'none'; 
            };
        }

        // В. Закрытие по клику ВНЕ окна
        window.addEventListener('click', (e) => {
            if (e.target == contactModal) {
                contactModal.style.display = 'none';
            }
        });
    }

    // 3. Contact Form AJAX
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
                    // Прячем форму, показываем успех
                    if (formContainer) formContainer.style.display = 'none';
                    if (successContainer) successContainer.style.display = 'block';
                    this.reset(); // Очищаем поля
                }
            });
        };
    }
});