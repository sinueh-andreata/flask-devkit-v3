const form = document.getElementById('formprodutos');
const respostaDiv = document.getElementById('resposta');

function _getCsrfToken() {
    const elById = document.getElementById('csrf_token');
    if (elById && elById.value) return elById.value;
}

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const nome = document.getElementById('nome').value.trim();
    const precoVal = document.getElementById('preco').value;
    const estoqueVal = document.getElementById('estoque').value;

    if (!nome || precoVal === '' || estoqueVal === '') {
        respostaDiv.innerHTML = `<p>Preencha nome, preço e estoque.</p>`;
        return;
    }

    const produto = { nome, preco: precoVal, estoque: estoqueVal };
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