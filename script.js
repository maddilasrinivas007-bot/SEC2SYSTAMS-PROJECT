// ===========================
// DOM ELEMENTS
// ===========================

const navbar = document.querySelector('.navbar');
const navLinks = document.querySelectorAll('.nav-link');
const pages = document.querySelectorAll('.page');
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');
const modal = document.getElementById('enrollModal');
const closeBtn = document.querySelector('.close');
const enrollmentForm = document.getElementById('enrollmentForm');
const loginForm = document.getElementById('loginForm');
const contactForm = document.getElementById('contactForm');
const filterButtons = document.querySelectorAll('.filter-btn');
const courseCards = document.querySelectorAll('.course-card');
const exploreBtn = document.getElementById('exploreBtn');

// ===========================
// NAVIGATION FUNCTIONALITY
// ===========================

navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        
        // Remove active class from all links
        navLinks.forEach(l => l.classList.remove('active'));
        
        // Add active class to clicked link
        link.classList.add('active');
        
        // Get section name
        const sectionName = link.getAttribute('data-section');
        
        // Hide all pages
        pages.forEach(page => {
            page.classList.remove('active');
            page.classList.add('hidden');
        });
        
        // Show selected page
        const selectedPage = document.getElementById(sectionName);
        if (selectedPage) {
            selectedPage.classList.remove('hidden');
            selectedPage.classList.add('active');
        }
        
        // Close hamburger menu
        navMenu.classList.remove('active');
        hamburger.classList.remove('active');
        
        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
});

// ===========================
// HAMBURGER MENU
// ===========================

hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
});

// Close hamburger menu when clicking outside
document.addEventListener('click', (e) => {
    if (!e.target.closest('.nav-container')) {
        hamburger.classList.remove('active');
        navMenu.classList.remove('active');
    }
});

// ===========================
// MODAL FUNCTIONALITY
// ===========================

function openEnrollModal(courseName) {
    document.getElementById('courseNameModal').textContent = courseName;
    modal.classList.add('show');
    document.body.style.overflow = 'hidden';
}

function closeEnrollModal() {
    modal.classList.remove('show');
    document.body.style.overflow = 'auto';
}

closeBtn.addEventListener('click', closeEnrollModal);

modal.addEventListener('click', (e) => {
    if (e.target === modal) {
        closeEnrollModal();
    }
});

// Close modal on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeEnrollModal();
    }
});

// ===========================
// FORM SUBMISSIONS
// ===========================

enrollmentForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const name = document.getElementById('enrollName').value;
    const email = document.getElementById('enrollEmail').value;
    const phone = document.getElementById('enrollPhone').value;
    const experience = document.getElementById('enrollExperience').value;
    
    // Here you would send this data to a server
    console.log('Enrollment Submitted:', { name, email, phone, experience });
    
    // Show success message
    showNotification('Success! Enrollment completed. We will contact you soon.', 'success');
    
    // Reset form
    enrollmentForm.reset();
    
    // Close modal
    closeEnrollModal();
});

loginForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    // Here you would send this data to a server
    console.log('Login Submitted:', { email, password });
    
    showNotification('Login successful! Welcome back.', 'success');
    
    // Reset form
    loginForm.reset();
    
    // Redirect to dashboard
    setTimeout(() => {
        document.querySelector('[data-section="home"]').click();
    }, 1000);
});

contactForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const name = document.getElementById('name').value;
    const email = document.getElementById('contactEmail').value;
    const subject = document.getElementById('subject').value;
    const message = document.getElementById('message').value;
    
    // Here you would send this data to a server
    console.log('Contact Submitted:', { name, email, subject, message });
    
    showNotification('Thank you! We will get back to you soon.', 'success');
    
    // Reset form
    contactForm.reset();
});

// ===========================
// COURSE FILTERING
// ===========================

filterButtons.forEach(button => {
    button.addEventListener('click', () => {
        // Remove active class from all buttons
        filterButtons.forEach(btn => btn.classList.remove('active'));
        
        // Add active class to clicked button
        button.classList.add('active');
        
        // Get filter value
        const filter = button.getAttribute('data-filter');
        
        // Filter courses
        courseCards.forEach(card => {
            if (filter === 'all') {
                card.classList.remove('hidden-card');
                setTimeout(() => {
                    card.style.animation = 'fadeIn 0.5s ease forwards';
                }, 0);
            } else {
                const category = card.getAttribute('data-category');
                if (category === filter) {
                    card.classList.remove('hidden-card');
                    setTimeout(() => {
                        card.style.animation = 'fadeIn 0.5s ease forwards';
                    }, 0);
                } else {
                    card.classList.add('hidden-card');
                }
            }
        });
    });
});

// ===========================
// REGISTER LINK
// ===========================

document.getElementById('registerLink').addEventListener('click', (e) => {
    e.preventDefault();
    
    // Show enrollment modal
    openEnrollModal('SEC2SYSTEMS Training Program');
    
    // Also navigate to training page
    setTimeout(() => {
        document.querySelector('[data-section="training"]').click();
    }, 500);
});

// ===========================
// EXPLORE BUTTON
// ===========================

exploreBtn.addEventListener('click', () => {
    document.querySelector('[data-section="training"]').click();
});

// ===========================
// NOTIFICATION SYSTEM
// ===========================

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: ${type === 'success' ? '#10b981' : '#3b82f6'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        z-index: 3000;
        animation: slideDown 0.3s ease;
        font-weight: 500;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    `;
    
    document.body.appendChild(notification);
    
    // Remove notification after 4 seconds
    setTimeout(() => {
        notification.style.animation = 'slideUp 0.3s ease forwards';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 4000);
}

// ===========================
// SMOOTH SCROLL HANDLING
// ===========================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#' && href !== '#home' && href !== '#training' && href !== '#about' && href !== '#contact' && href !== '#login') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        }
    });
});

// ===========================
// LAZY LOADING ANIMATIONS
// ===========================

const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'fadeIn 0.5s ease forwards';
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe course cards
courseCards.forEach(card => {
    observer.observe(card);
});

// Observe highlight cards
document.querySelectorAll('.highlight-card').forEach(card => {
    observer.observe(card);
});

// Observe testimonial cards
document.querySelectorAll('.testimonial-card').forEach(card => {
    observer.observe(card);
});

// ===========================
// NAVBAR BACKGROUND ON SCROLL
// ===========================

window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        navbar.style.background = 'rgba(15, 15, 30, 0.98)';
        navbar.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.3)';
    } else {
        navbar.style.background = 'rgba(15, 15, 30, 0.95)';
        navbar.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
    }
});

// ===========================
// INPUT FOCUS EFFECTS
// ===========================

document.querySelectorAll('.form-group input, .form-group textarea, .form-group select').forEach(input => {
    input.addEventListener('focus', function() {
        this.parentElement.style.transform = 'scale(1.02)';
    });
    
    input.addEventListener('blur', function() {
        this.parentElement.style.transform = 'scale(1)';
    });
});

// ===========================
// COUNTER ANIMATION
// ===========================

function animateCounter(element, target, duration = 2000) {
    const start = 0;
    const increment = target / (duration / 16);
    let current = start;
    
    const counter = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = target + '+';
            clearInterval(counter);
        } else {
            element.textContent = Math.floor(current) + '+';
        }
    }, 16);
}

// Animate stats on page load
const statCards = document.querySelectorAll('.stat-card h3');
let animated = false;

const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting && !animated) {
            animated = true;
            animateCounter(statCards[0], 5000);
            animateCounter(statCards[1], 95);
            animateCounter(statCards[2], 50);
            animateCounter(statCards[3], 10);
            statsObserver.unobserve(entry.target);
        }
    });
});

if (statCards.length > 0) {
    statsObserver.observe(statCards[0].parentElement);
}

// ===========================
// MOBILE RESPONSIVENESS
// ===========================

function handleResize() {
    if (window.innerWidth > 768) {
        navMenu.classList.remove('active');
        hamburger.classList.remove('active');
    }
}

window.addEventListener('resize', handleResize);

// ===========================
// KEYBOARD NAVIGATION
// ===========================

document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + K to open search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        // Could implement search functionality here
    }
    
    // Tab key for accessibility
    if (e.key === 'Tab') {
        // Focus management for modals
        if (modal.classList.contains('show')) {
            const focusableElements = modal.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
            const firstElement = focusableElements[0];
            const lastElement = focusableElements[focusableElements.length - 1];
            
            if (e.shiftKey) {
                if (document.activeElement === firstElement) {
                    lastElement.focus();
                    e.preventDefault();
                }
            } else {
                if (document.activeElement === lastElement) {
                    firstElement.focus();
                    e.preventDefault();
                }
            }
        }
    }
});

// ===========================
// PAGE INITIALIZATION
// ===========================

document.addEventListener('DOMContentLoaded', () => {
    // Set home as default active page
    const homeLink = document.querySelector('[data-section="home"]');
    if (homeLink) {
        homeLink.classList.add('active');
    }
    
    // Log app status
    console.log('%cSEC2SYSTEMS Training Platform', 'color: #00d4ff; font-size: 20px; font-weight: bold;');
    console.log('%cWelcome to the training platform!', 'color: #667eea; font-size: 14px;');
});

// ===========================
// DEBUGGING HELPERS (Development only)
// ===========================

window.SEC2SYSTEMS = {
    openEnrollModal,
    closeEnrollModal,
    showNotification,
    version: '1.0.0',
    name: 'SEC2SYSTEMS Training Platform'
};

// Add console helpers
console.log('Available commands: SEC2SYSTEMS.openEnrollModal(courseName), SEC2SYSTEMS.closeEnrollModal(), SEC2SYSTEMS.showNotification(message, type)');

// ===========================
// PERFORMANCE OPTIMIZATION
// ===========================

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Throttle function
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Apply throttle to scroll event
window.addEventListener('scroll', throttle(() => {
    // Scroll handlers can be added here
}, 100));

// ===========================
// DATA VALIDATION
// ===========================

function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePhone(phone) {
    const re = /^[0-9]{10,}$/;
    return re.test(phone.replace(/\D/g, ''));
}

// Add custom validation to forms
enrollmentForm.addEventListener('submit', (e) => {
    const email = document.getElementById('enrollEmail').value;
    const phone = document.getElementById('enrollPhone').value;
    
    if (!validateEmail(email)) {
        e.preventDefault();
        showNotification('Please enter a valid email address', 'error');
        return;
    }
    
    if (!validatePhone(phone)) {
        e.preventDefault();
        showNotification('Please enter a valid phone number', 'error');
        return;
    }
});

// ===========================
// SERVICE WORKER (PWA Support)
// ===========================

if ('serviceWorker' in navigator) {
    // Service worker registration can be added here for offline support
}

// ===========================
// ACCESSIBILITY IMPROVEMENTS
// ===========================

// Add skip to main content link
const skipLink = document.createElement('a');
skipLink.href = '#main';
skipLink.textContent = 'Skip to main content';
skipLink.style.cssText = `
    position: absolute;
    top: -40px;
    left: 0;
    background: #00d4ff;
    color: #0f0f1e;
    padding: 8px;
    text-decoration: none;
    z-index: 100;
`;

skipLink.addEventListener('focus', () => {
    skipLink.style.top = '0';
});

skipLink.addEventListener('blur', () => {
    skipLink.style.top = '-40px';
});

document.body.insertBefore(skipLink, document.body.firstChild);

// ===========================
// ERROR HANDLING
// ===========================

window.addEventListener('error', (event) => {
    console.error('Error:', event.error);
    // Could send error logs to server
});

// Unhandled promise rejection handler
window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled rejection:', event.reason);
    // Could send error logs to server
});

// ===========================
// ANALYTICS & TRACKING (Optional)
// ===========================

// Example: Track page views
function trackPageView(pageName) {
    console.log(`Page viewed: ${pageName}`);
    // Could send to Google Analytics or other tracking service
}

// Track navigation
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        trackPageView(link.getAttribute('data-section'));
    });
});

// ===========================
// INITIALIZATION COMPLETE
// ===========================

console.log('✓ SEC2SYSTEMS platform loaded successfully');
