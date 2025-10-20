fetch('/csrf-token')
    .then(response => response.json())
    .then(data => {
        const form = document.querySelector('form');
        const csrfInput = document.createElement('input');
        csrfInput.type = 'hidden';
        csrfInput.name = 'csrf_token';
        csrfInput.value = data.csrf_token;
        form.insertBefore(csrfInput, form.firstChild);
    });

function getCsrfToken() {
    const el = document.querySelector('input[name="csrf_token"]');
    return el ? el.value : null;
}

if (typeof window !== 'undefined') {
    window.getCsrfToken = getCsrfToken;
}