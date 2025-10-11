document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('.needs-validation');
    const button = form?.querySelector('.submit-button');

    if (!form || !button) return;

    button.addEventListener('click', event => {
        event.preventDefault();

        if (!form.checkValidity()) {
            form.classList.add('was-validated');
            return;
        }

        form.submit(); // real submission to Django's /checkout/
    });
});
