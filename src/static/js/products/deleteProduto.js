document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('deleteProdutoForm');
    const respostaDiv = document.getElementById('resposta');

    function _getCsrfToken() {
        if (typeof getCsrfToken === 'function') return getCsrfToken();
    }

    if (!form) {
        console.warn('deleteProduto: #deleteProdutoForm not found in DOM');
        return;
    }


    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        console.log('submit!');

        const produtoIdVal = form.elements['produto_id'].value;
        const produto_id = Number(produtoIdVal);

        if (!produto_id) {
            respostaDiv.innerHTML = `<p>Produto inválido.</p>`;
            return;
        }

        const csrfToken = _getCsrfToken();

        try {
            const response = await fetch(`/produtos/deletar/produto/${produto_id}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken || '',
                    'X-CSRF-Token': csrfToken || ''
                },
                credentials: 'same-origin'
            });

            if (response.ok) {
                respostaDiv.innerHTML = `<p>Produto deletado com sucesso.</p>`;
            } else {
                const errorData = await response.json();
                respostaDiv.innerHTML = `<p>Erro ao deletar produto: ${errorData.error || 'Erro desconhecido'}</p>`;
            }
        } catch (error) {
            respostaDiv.innerHTML = `<p>Erro na requisição: ${error.message}</p>`;
        }
    });
});