document.addEventListener('DOMContentLoaded', () => {
    // Form validation for signup
    const signupForm = document.querySelector('form[action="/signup"]');
    if (signupForm) {
        signupForm.addEventListener('submit', (e) => {
            const username = signupForm.querySelector('input[name="username"]').value;
            const email = signupForm.querySelector('input[name="email"]').value;
            const password = signupForm.querySelector('input[name="password"]').value;
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

            if (username.length < 3) {
                alert('Username must be at least 3 characters long.');
                e.preventDefault();
            } else if (!emailRegex.test(email)) {
                alert('Please enter a valid email address.');
                e.preventDefault();
            } else if (password.length < 6) {
                alert('Password must be at least 6 characters long.');
                e.preventDefault();
            }
        });
    }

    // Form validation for login
    const loginForm = document.querySelector('form[action="/login"]');
    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            const email = loginForm.querySelector('input[name="email"]').value;
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

            if (!emailRegex.test(email)) {
                alert('Please enter a valid email address.');
                e.preventDefault();
            }
        });
    }

    // Confirmation for file upload
    const sendFileForm = document.querySelector('form[action*="/send_file"]');
    if (sendFileForm) {
        sendFileForm.addEventListener('submit', (e) => {
            const fileInput = sendFileForm.querySelector('input[name="file"]');
            if (!fileInput.files.length) {
                alert('Please select a file to upload.');
                e.preventDefault();
            } else if (!confirm('Are you sure you want to send this file?')) {
                e.preventDefault();
            }
        });
    }

    // Validation for decrypt form
    const decryptForm = document.querySelector('form[action*="/decrypt_file"]');
    if (decryptForm) {
        decryptForm.addEventListener('submit', (e) => {
            const key = decryptForm.querySelector('input[name="key"]').value;
            const iv = decryptForm.querySelector('input[name="iv"]');
            
            if (!key) {
                alert('Please enter the encryption key.');
                e.preventDefault();
            } else if (iv && !iv.value) {
                alert('Please enter the IV for this algorithm.');
                e.preventDefault();
            }
        });
    }

    // Dynamic feedback for file input
    const fileInput = document.querySelector('input[name="file"]');
    if (fileInput) {
        fileInput.addEventListener('change', () => {
            const fileName = fileInput.files[0]?.name || 'No file selected';
            const label = fileInput.closest('form').querySelector('label[for="file"]');
            if (label) {
                label.textContent = `Selected: ${fileName}`;
            }
        });
    }
});

// Close button functionality
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('close-alert')) {
        const alert = e.target.closest('.alert');
        alert.style.animation = 'fadeOut 0.5s ease forwards';
        setTimeout(() => alert.remove(), 500);
    }
});