document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('formprodutos');
    const respostaDiv = document.getElementById('resposta');

function _getCsrfToken() {
    if (typeof getCsrfToken === 'function') return getCsrfToken();
}

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const nome = form.querySelector('#nome').value.trim();
    const precoVal = form.querySelector('#preco').value;
    const estoqueVal = form.querySelector('#estoque').value;
    const preco = Number(precoVal);
    const estoque = Number(estoqueVal);

    if (!nome || precoVal === '' || estoqueVal === '' || isNaN(preco) || isNaN(estoque)) {
        respostaDiv.innerHTML = `<p>Preencha nome, preço e estoque corretamente.</p>`;
        return;
    }

    const produto = { nome, preco, estoque };
    const csrfToken = _getCsrfToken();

    try {
        const response = await fetch('/produtos/novo/produto', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken || '',
                'X-CSRF-Token': csrfToken || ''
            },
            credentials: 'same-origin',
            body: JSON.stringify(produto)
        });

        const contentType = response.headers.get('content-type') || '';
        let data;
        if (contentType.includes('application/json')) {
            data = await response.json();
        } else {
            const text = await response.text();
            data = text ? { error: text } : { error: 'Resposta inválida do servidor' };
        }

        if (response.ok) {
            respostaDiv.innerHTML = `<p>Produto cadastrado com sucesso: ${data.nome}</p>`;
            form.reset();
        } else {
            respostaDiv.innerHTML = `<p>Erro ao cadastrar produto: ${data.error || 'Erro desconhecido'}</p>`;
        }
    } catch (error) {
        respostaDiv.innerHTML = `<p>Erro na requisição: ${error.message}</p>`;
    }
    });
});