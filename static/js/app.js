// ===== Global Helper Functions =====
const showNotification = (message, type = 'success') => {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('fade-out');
        setTimeout(() => notification.remove(), 500);
    }, 3000);
};

const handleApiError = (error) => {
    console.error('API Error:', error);
    showNotification('An error occurred. Please try again.', 'error');
};

// ===== DOM Ready Handler =====
document.addEventListener('DOMContentLoaded', function() {
    // ===== General Form Handling =====
    document.querySelectorAll('form[data-async]').forEach(form => {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            
            try {
                // Show loading state
                submitBtn.disabled = true;
                submitBtn.textContent = 'Processing...';
                
                const formData = new FormData(form);
                const response = await fetch(form.action, {
                    method: form.method,
                    body: formData
                });
                
                if (response.redirected) {
                    window.location.href = response.url;
                } else {
                    const result = await response.json();
                    if (result.success) {
                        showNotification(result.message || 'Operation successful');
                        if (form.dataset.resetOnSuccess !== 'false') {
                            form.reset();
                        }
                        if (result.redirect) {
                            setTimeout(() => {
                                window.location.href = result.redirect;
                            }, 1500);
                        }
                    } else {
                        showNotification(result.message || 'Operation failed', 'error');
                    }
                }
            } catch (error) {
                handleApiError(error);
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = originalText;
            }
        });
    });

    // ===== Game Initialization =====
    if (document.getElementById('hangman-game')) {
        initHangmanGame();
    }

    if (document.getElementById('math-quiz-game')) {
        initMathQuizGame();
    }

    if (document.getElementById('rps-game')) {
        initRPSGame();
    }

    // ===== Navigation Active State =====
    const currentPath = window.location.pathname;
    document.querySelectorAll('nav a').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
});

// ===== Profile Edit Handling =====
if (document.getElementById('profile-form')) {
    document.getElementById('profile-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        const submitBtn = this.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        
        try {
            submitBtn.disabled = true;
            submitBtn.textContent = 'Updating...';
            
            const response = await fetch(this.action, {
                method: 'POST',
                body: formData
            });
            
            if (response.redirected) {
                window.location.href = response.url;
            } else {
                const result = await response.json();
                if (result.success) {
                    showNotification('Profile updated successfully!');
                } else {
                    showNotification(result.message || 'Failed to update profile', 'error');
                }
            }
        } catch (error) {
            handleApiError(error);
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
        }
    });
}

// ===== Admin User Deletion =====
document.querySelectorAll('.delete-user-btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
        e.preventDefault();
        
        if (confirm('Are you sure you want to delete this user?')) {
            const form = this.closest('form');
            fetch(form.action, {
                method: 'POST',
                body: new FormData(form)
            })
            .then(response => {
                if (response.redirected) {
                    window.location.href = response.url;
                } else {
                    return response.json();
                }
            })
            .then(data => {
                if (data && data.success) {
                    showNotification('User deleted successfully');
                    form.closest('tr').remove();
                }
            })
            .catch(handleApiError);
        }
    });
});