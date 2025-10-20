const formProdutos = document.getElementById('produtosForm');

document.addEventListener('DOMContentLoaded', () => {
    if (!formProdutos) {
        console.warn('getProduto: #produtosForm not found in DOM');
        return;
    }
    fetchProdutos().then(() => console.log('getProduto: fetch finished'));
});

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
            if (Array.isArray(produtos)) {
                formProdutos.innerHTML = produtos.map(p => `\n                    <div class="produto">\n                        <h3>${p.nome}</h3>\n                        <p>Preço: ${p.preco}</p>\n                        <p>Estoque: ${p.estoque}</p>\n                    </div>\n                `).join('');
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