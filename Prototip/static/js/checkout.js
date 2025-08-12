
(() => {
    const forms = document.querySelectorAll('.needs-validation');

    Array.from(forms).forEach(form => {
        const button = form.querySelector('.submit-button');

        if (button) {
            button.addEventListener('click', () => {
                if (!form.checkValidity()) {
                    form.classList.add('was-validated');
                } else {
                    window.location.href = 'successful_payment.html';
                }
            });
        }
    });
})();

