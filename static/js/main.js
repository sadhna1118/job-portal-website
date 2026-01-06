/**
 * Main JavaScript file for Job Portal
 */

// Auto-hide flash messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.flash');
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            message.style.animation = 'slideOut 0.3s ease-out forwards';
            setTimeout(function() {
                message.remove();
            }, 300);
        }, 5000);
    });
});

// Add slideOut animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Form validation helpers
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePhone(phone) {
    const re = /^[\d\s\-\+\(\)]+$/;
    return phone.length >= 10 && re.test(phone);
}

// Password strength indicator
function checkPasswordStrength(password) {
    let strength = 0;
    if (password.length >= 8) strength++;
    if (password.match(/[a-z]+/)) strength++;
    if (password.match(/[A-Z]+/)) strength++;
    if (password.match(/[0-9]+/)) strength++;
    if (password.match(/[$@#&!]+/)) strength++;
    
    return strength;
}

// Debounce function for search
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

// Format date to relative time
function timeAgo(date) {
    const now = new Date();
    const past = new Date(date);
    const diffInSeconds = Math.floor((now - past) / 1000);
    
    if (diffInSeconds < 60) return 'just now';
    if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)} minutes ago`;
    if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)} hours ago`;
    if (diffInSeconds < 604800) return `${Math.floor(diffInSeconds / 86400)} days ago`;
    if (diffInSeconds < 2592000) return `${Math.floor(diffInSeconds / 604800)} weeks ago`;
    return past.toLocaleDateString();
}

// Loading indicator
function showLoading() {
    const loader = document.createElement('div');
    loader.id = 'loading-overlay';
    loader.innerHTML = `
        <div style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; 
                    background: rgba(0,0,0,0.5); display: flex; align-items: center; 
                    justify-content: center; z-index: 9999;">
            <div style="background: white; padding: 2rem; border-radius: 0.5rem; 
                        text-align: center;">
                <div style="width: 50px; height: 50px; border: 4px solid #f3f4f6; 
                            border-top-color: #1560BD; border-radius: 50%; 
                            animation: spin 1s linear infinite; margin: 0 auto;"></div>
                <p style="margin-top: 1rem; color: #64748B;">Loading...</p>
            </div>
        </div>
    `;
    document.body.appendChild(loader);
}

function hideLoading() {
    const loader = document.getElementById('loading-overlay');
    if (loader) loader.remove();
}

// Add spin animation
const spinStyle = document.createElement('style');
spinStyle.textContent = `
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
`;
document.head.appendChild(spinStyle);

// Smooth scroll to top
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Add scroll to top button
window.addEventListener('scroll', function() {
    const scrollBtn = document.getElementById('scroll-to-top');
    if (window.pageYOffset > 300) {
        if (!scrollBtn) {
            const btn = document.createElement('button');
            btn.id = 'scroll-to-top';
            btn.innerHTML = '<i class="icon-arrow-up"></i>';
            btn.style.cssText = `
                position: fixed; bottom: 2rem; right: 2rem; 
                background: var(--color-primary); color: white;
                border: none; border-radius: 50%; width: 50px; height: 50px;
                cursor: pointer; box-shadow: var(--shadow-lg);
                display: flex; align-items: center; justify-content: center;
                z-index: 1000; transition: all 0.3s;
            `;
            btn.onclick = scrollToTop;
            document.body.appendChild(btn);
        }
    } else {
        if (scrollBtn) scrollBtn.remove();
    }
});

// Console welcome message
console.log('%c🚀 Job Portal', 'font-size: 20px; font-weight: bold; color: #1560BD;');
console.log('%cWelcome to Job Portal! Connect with top companies and discover opportunities.', 'font-size: 14px; color: #64748B;');