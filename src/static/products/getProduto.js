document.addEventListener('DOMContentLoaded', () => {
    const formProdutos = document.getElementById('produtosForm');

    function _getCsrfToken() {
        if (typeof getCsrfToken === 'function') return getCsrfToken();
    }

    async function fetchProdutos() {
        const csrfToken = _getCsrfToken();
        try {
            const response = await fetch('/produtos/all/products', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken || '',
                    'X-CSRF-Token': csrfToken || ''
                },
                credentials: 'same-origin'
            });
            if (response.ok) {
                const produtos = await response.json();
                if (Array.isArray(produtos) && formProdutos) {
                    formProdutos.innerHTML = produtos.map(p => 
                        `<div class="produto">
                            <h3>${p.nome}</h3>
                            <p>Preço: ${p.preco}</p>
                            <p>Estoque: ${p.estoque}</p>
                        </div>`
                    ).join('');
                }
                return produtos;
            } else {
                console.error('Erro ao buscar produtos:', response.statusText);
                return [];
            }
        } catch (error) {
            console.error('Erro na requisição:', error);
            return [];
        }
    }

    fetchProdutos().then(() => console.log('getProduto: fetch finished'));
});