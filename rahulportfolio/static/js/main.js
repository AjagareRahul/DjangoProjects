/**
 * Main JavaScript for Portfolio Website - Modern Digital Edition
 * For Ajagare Rahul - Python & Django Developer
 * Enhanced with modern animations, interactions, and features
 */

document.addEventListener('DOMContentLoaded', function() {
    // ==========================================
    // Initialize AOS Animation Library
    // ==========================================
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            once: true,
            offset: 100,
            easing: 'ease-out-cubic'
        });
    }
    
    // ==========================================
    // Navbar Scroll Effect
    // ==========================================
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
        
        // Initial check
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        }
    }
    
    // ==========================================
    // Back to Top Button
    // ==========================================
    const backToTopBtn = document.getElementById('backToTop');
    if (backToTopBtn) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 300) {
                backToTopBtn.classList.add('show');
            } else {
                backToTopBtn.classList.remove('show');
            }
        });
        
        backToTopBtn.addEventListener('click', function(e) {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    // ==========================================
    // Auto-hide Alerts
    // ==========================================
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // ==========================================
    // Smooth Scroll for Anchor Links
    // ==========================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // ==========================================
    // Form Validation
    // ==========================================
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
    
    // ==========================================
    // Contact Form AJAX Submission
    // ==========================================
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            
            // Show loading state
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Sending...';
            submitBtn.disabled = true;
            
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showAlert('success', 'Message sent successfully! I\'ll get back to you soon.');
                    contactForm.reset();
                } else {
                    showAlert('danger', 'Failed to send message. Please try again.');
                }
            })
            .catch(error => {
                showAlert('danger', 'An error occurred. Please try again.');
            })
            .finally(() => {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            });
        });
    }
    
    // ==========================================
    // Search Functionality
    // ==========================================
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            const cards = document.querySelectorAll('.project-card, .blog-card, .skill-card');
            
            cards.forEach(card => {
                const title = card.querySelector('.card-title, h5, .skill-title');
                if (title) {
                    const titleText = title.textContent.toLowerCase();
                    const text = card.querySelector('.card-text');
                    const textText = text ? text.textContent.toLowerCase() : '';
                    
                    if (titleText.includes(searchTerm) || textText.includes(searchTerm)) {
                        card.style.display = '';
                        card.style.opacity = '1';
                    } else {
                        card.style.opacity = '0.3';
                    }
                }
            });
        });
    }
    
    // ==========================================
    // Lazy Loading Images
    // ==========================================
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                        img.classList.add('loaded');
                    }
                    imageObserver.unobserve(img);
                }
            });
        }, {
            rootMargin: '50px'
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            img.classList.add('lazy-load');
            imageObserver.observe(img);
        });
    }
    
    // ==========================================
    // Counter Animation
    // ==========================================
    const counters = document.querySelectorAll('.counter');
    if (counters.length > 0) {
        const counterObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const counter = entry.target;
                    const target = parseInt(counter.dataset.target);
                    const duration = 2000;
                    const increment = target / (duration / 16);
                    let current = 0;
                    
                    const updateCounter = () => {
                        current += increment;
                        if (current < target) {
                            counter.textContent = Math.ceil(current);
                            requestAnimationFrame(updateCounter);
                        } else {
                            counter.textContent = target;
                        }
                    };
                    
                    updateCounter();
                    counterObserver.unobserve(counter);
                }
            });
        }, {
            threshold: 0.5
        });
        
        counters.forEach(counter => {
            counterObserver.observe(counter);
        });
    }
    
    // ==========================================
    // Progress Bar Animation
    // ==========================================
    const progressBars = document.querySelectorAll('.progress-bar');
    if (progressBars.length > 0) {
        const progressObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const bar = entry.target;
                    const targetWidth = bar.style.width;
                    bar.style.width = '0';
                    setTimeout(() => {
                        bar.style.width = targetWidth;
                    }, 100);
                    progressObserver.unobserve(bar);
                }
            });
        }, {
            threshold: 0.5
        });
        
        progressBars.forEach(bar => {
            progressObserver.observe(bar);
        });
    }
    
    // ==========================================
    // Card Hover Effects
    // ==========================================
    const cards = document.querySelectorAll('.card, .service-card, .skill-card, .project-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
        });
        card.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
    });
    
    // ==========================================
    // Navbar Active Link Highlight
    // ==========================================
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
    
    // ==========================================
    // Scroll Reveal Animation
    // ==========================================
    const revealElements = document.querySelectorAll('.reveal');
    if (revealElements.length > 0) {
        const revealObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });
        
        revealElements.forEach(el => revealObserver.observe(el));
    }
    
    // ==========================================
    // Typing Animation (if applicable)
    // ==========================================
    const typingElements = document.querySelectorAll('.typing-text');
    typingElements.forEach(element => {
        const text = element.textContent;
        element.textContent = '';
        let i = 0;
        
        const typeWriter = () => {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, 100);
            }
        };
        
        // Start typing when element is in view
        const typingObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    setTimeout(typeWriter, 500);
                    typingObserver.unobserve(element);
                }
            });
        });
        
        typingObserver.observe(element);
    });
    
    // ==========================================
    // Parallax Effect (optional)
    // ==========================================
    const parallaxElements = document.querySelectorAll('[data-parallax]');
    if (parallaxElements.length > 0 && window.matchMedia('(min-width: 992px)').matches) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            parallaxElements.forEach(el => {
                const speed = el.dataset.parallax || 0.5;
                el.style.transform = `translateY(${scrolled * speed}px)`;
            });
        });
    }
});

// ==========================================
// Helper: Show Alert
// ==========================================
function showAlert(type, message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-5 z-index-9999`;
    alertDiv.setAttribute('role', 'alert');
    alertDiv.innerHTML = `
        <strong>${type === 'success' ? '<i class="fas fa-check-circle me-2"></i>' : '<i class="fas fa-exclamation-circle me-2"></i>'}
        ${message}</strong>
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// ==========================================
// Helper: CSRF Token
// ==========================================
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Set CSRF token for AJAX
const csrfToken = getCookie('csrftoken');
if (csrfToken && typeof $ !== 'undefined') {
    $.ajaxSetup({
        headers: {
            'X-CSRFToken': csrfToken
        }
    });
}

// ==========================================
// Preloader (optional)
// ==========================================
window.addEventListener('load', function() {
    const preloader = document.querySelector('.page-loader');
    if (preloader) {
        preloader.classList.add('fade-out');
        setTimeout(() => {
            preloader.remove();
        }, 500);
    }
});

// ==========================================
// Smooth Page Transitions
// ==========================================
document.querySelectorAll('a:not([href^="#"]):not([href^="mailto"]):not([href^="tel"])').forEach(link => {
    link.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        if (href && !href.startsWith('http') && !href.startsWith('//')) {
            // Add fade-out effect before navigation
            document.body.style.opacity = '0';
            document.body.style.transition = 'opacity 0.3s ease';
        }
    });
});
