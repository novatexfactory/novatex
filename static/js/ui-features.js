// static/js/ui-features.js

document.addEventListener('DOMContentLoaded', function() {
    
    // ==========================================
    // 1. STICKY HEADER EFFECT
    // ==========================================
    const header = document.querySelector('.site-header');
    if (header) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                header.classList.add('header-scrolled');
            } else {
                header.classList.remove('header-scrolled');
            }
        });
    }

    // ==========================================
    // 2. SCROLL TO TOP BUTTON
    // ==========================================
    const scrollBtn = document.getElementById('scrollToTopBtn');
    if (scrollBtn) {
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
    }

    // ==========================================
    // 3. AGE VERIFICATION MODAL
    // ==========================================
    const ageModal = document.getElementById('ageModal');
    if (ageModal) {
        const btnYes = document.getElementById('btnAgeYes');
        if (localStorage.getItem('ageVerified') === 'true') {
            ageModal.style.display = 'none';
        } else {
            ageModal.style.display = 'flex';
        }

        if (btnYes) {
            btnYes.addEventListener('click', function() {
                localStorage.setItem('ageVerified', 'true');
                ageModal.classList.add('hidden');
                setTimeout(() => { ageModal.style.display = 'none'; }, 500);
            });
        }
    }

    // ==========================================
    // 4. CONTACT MODAL (ИСПРАВЛЕННАЯ ВЕРСИЯ)
    // ==========================================
    
    // 1. Ищем кнопку более универсально (по части ссылки #contact)
    // Это сработает и для "/#contact", и для "#contact"
    const navContactLink = document.querySelector('a[href$="#contact"]'); 
    const contactModal = document.getElementById('contactModal');
    // Ищем кнопку закрытия внутри модалки (добавьте класс или ID к крестику в HTML, если нет)
    const closeContactBtn = contactModal ? contactModal.querySelector('.close-btn, .modal-close') : null;

    if (navContactLink && contactModal) {
        // Открытие
        navContactLink.addEventListener('click', function(e) {
            e.preventDefault();
            
            // --- ДОБАВЛЕННЫЙ БЛОК: СБРОС СОСТОЯНИЯ ---
            // Перед тем как показать окно, мы принудительно возвращаем всё "как было"
            const formContainer = document.getElementById('contact-form-container');
            const successContainer = document.getElementById('form-success-container');
            const contactForm = document.getElementById('contact-form-modal');

            if (formContainer && successContainer) {
                formContainer.style.display = 'block';   // Показываем форму
                successContainer.style.display = 'none'; // Скрываем "Спасибо"
            }
            
            // Если нужно очистить поля при повторном открытии (опционально)
            if (contactForm) {
                // contactForm.reset(); // Раскомментируйте, если хотите стирать старый текст
            }
            // ------------------------------------------

            contactModal.style.display = 'flex';
        });

        // Закрытие по крестику (если он есть)
        if (closeContactBtn) {
            closeContactBtn.addEventListener('click', function() {
                contactModal.style.display = 'none';
            });
        }

        // Закрытие по клику вне окна (как в Tech Modal)
        window.addEventListener('click', function(e) {
            if (e.target === contactModal) {
                contactModal.style.display = 'none';
            }
        });
    }

    // ==========================================
    // 5. TECHNOLOGY MODAL (FIXED)
    // ==========================================
    const techModal = document.getElementById('techModal');
    const closeTechBtn = document.getElementById('closeTechModal');
    
    // Ищем кнопку по тексту "OUR TECHNOLOGY", так как у нее нет ID
    const allLinks = document.querySelectorAll('a');
    let openTechBtn = null;

    for (let link of allLinks) {
        if (link.textContent.trim() === "OUR TECHNOLOGY") {
            openTechBtn = link;
            break; 
        }
    }

    if (openTechBtn && techModal) {
        openTechBtn.addEventListener('click', function(e) {
            e.preventDefault(); // Останавливаем прыжок вверх
            techModal.style.display = 'flex'; // Показываем окно
        });

        // Закрытие по крестику
        if (closeTechBtn) {
            closeTechBtn.addEventListener('click', function() {
                techModal.style.display = 'none';
            });
        }

        // Закрытие по клику вне окна
        window.addEventListener('click', function(e) {
            if (e.target === techModal) {
                techModal.style.display = 'none';
            }
        });
    }
});