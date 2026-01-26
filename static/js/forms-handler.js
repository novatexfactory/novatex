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
    
    // Элементы внутри модального окна
    const formContainer = document.getElementById('contact-form-container');
    const successContainer = document.getElementById('form-success-container');

    // === FIX 1: Расширенный список триггеров ===
    // Добавил a[href="#contact"] и a[href="/contact/"], чтобы точно поймать меню
    const openTriggers = document.querySelectorAll('.contact-cta-btn, #openContactModal, a[href="/contact"], a[href="#contact"]');

    if (contactModal) {
        openTriggers.forEach(btn => {
            btn.addEventListener('click', function(e) {
                // Если это ссылка, блокируем переход
                if (this.tagName === 'A') e.preventDefault(); 
                
                // СБРОС СОСТОЯНИЯ: Показываем форму заново
                if (formContainer) formContainer.style.display = 'block';
                if (successContainer) successContainer.style.display = 'none';

                // Показываем окно (Bootstrap обычно делает это сам, но этот код страхует)
                contactModal.style.display = 'flex'; 
            });
        });

        // Закрытие по крестику
        if (closeBtn) {
            closeBtn.onclick = () => { 
                contactModal.style.display = 'none'; 
            };
        }

        // Закрытие по клику ВНЕ окна
        window.addEventListener('click', (e) => {
            if (e.target == contactModal) {
                contactModal.style.display = 'none';
            }
        });
    }

    // 3. Contact Form AJAX (FIXED)
    // === FIX 2: Используем querySelectorAll для захвата ВСЕХ форм ===
    // Ищем формы и по ID (даже если дублируются), и по классу .contact-form-modal
    const contactForms = document.querySelectorAll('#contact-form-modal, .contact-form-modal');
    
    contactForms.forEach(form => {
        form.onsubmit = function(e) {
            e.preventDefault(); // Самое важное: отменяем перезагрузку страницы
            
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
                    this.reset(); // Очищаем поля текущей формы
                } else {
                    alert('Error sending message. Please try again.');
                }
            })
            .catch(error => console.error('Error:', error));
        };
    });
});