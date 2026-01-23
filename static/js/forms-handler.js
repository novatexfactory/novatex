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

    // 2. Contact Modal Logic (Обновлено для работы со ссылками)
    const contactModal = document.getElementById('contactModal');
    const closeBtn = document.getElementById('closeContactModal');

    // А. Логика ОТКРЫТИЯ (Ловим все кнопки контактов)
    // Мы ищем:
    // 1. Кнопки с классом .contact-cta-btn (наша ссылка в футере)
    // 2. Элемент с ID #openContactModal (кнопка в меню, если есть)
    // 3. Любые ссылки, ведущие на "/contact"
    const openTriggers = document.querySelectorAll('.contact-cta-btn, #openContactModal, a[href="/contact"]');

    if (contactModal) {
        openTriggers.forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.preventDefault(); // ОТМЕНЯЕМ переход на страницу 404
                contactModal.style.display = 'flex'; // Открываем окно
            });
        });

        // Б. Логика ЗАКРЫТИЯ (Крестик)
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
                    document.getElementById('contact-form-container').style.display = 'none';
                    document.getElementById('form-success-container').style.display = 'block';
                    this.reset();
                }
            });
        };
    }
});