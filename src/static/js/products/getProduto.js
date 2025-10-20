document.addEventListener('DOMContentLoaded', () => {
    const formProdutos = document.getElementById('produtosForm');
    const updateSection = document.getElementById('updateSection');
    const closeUpdateBtn = document.getElementById('closeUpdate');

    function _getCsrfToken() {
        if (typeof getCsrfToken === 'function') return getCsrfToken();
    }

    function preencherFormulario(produto) {
        // Preenche o formulário de atualização
        document.getElementById('produto_id').value = produto.id;
        document.getElementById('nome_update').value = produto.nome;
        document.getElementById('preco_update').value = produto.preco;
        document.getElementById('estoque_update').value = produto.estoque;

        updateSection.classList.remove('hidden');
        
        updateSection.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'center' 
        });
    }

    if (closeUpdateBtn) {
        closeUpdateBtn.addEventListener('click', () => {
            updateSection.classList.add('hidden');
        });
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
                    formProdutos.innerHTML = '';
                    produtos.forEach(p => {
                        const div = document.createElement('div');
                        div.className = "produto p-4 border border-gray-200 rounded-lg hover:border-blue-400 hover:shadow-md transition cursor-pointer";
                        div.dataset.produto = JSON.stringify(p);

                        const flex = document.createElement('div');
                        flex.className = "flex justify-between items-start";

                        const info = document.createElement('div');
                        info.className = "flex-1";

                        const h3 = document.createElement('h3');
                        h3.className = "text-lg font-semibold text-gray-800";
                        h3.textContent = p.nome;

                        const preco = document.createElement('p');
                        preco.className = "text-gray-600 mt-1";
                        preco.textContent = `Preço: R$ ${parseFloat(p.preco).toFixed(2)}`;

                        const estoque = document.createElement('p');
                        estoque.className = "text-gray-600";
                        estoque.textContent = `Estoque: ${p.estoque} unidades`;

                        info.appendChild(h3);
                        info.appendChild(preco);
                        info.appendChild(estoque);

                        const span = document.createElement('span');
                        span.className = "text-sm text-gray-400";
                        span.textContent = `#${p.id}`;

                        flex.appendChild(info);
                        flex.appendChild(span);
                        div.appendChild(flex);

                        div.addEventListener('click', async function() {
                            const produto = JSON.parse(this.dataset.produto);
                            try {
                                const csrfToken = _getCsrfToken();
                                const resp = await fetch(`/produtos/produto/${produto.id}`, {
                                    method: 'GET',
                                    headers: {
                                        'Content-Type': 'application/json',
                                        'X-CSRFToken': csrfToken || '',
                                        'X-CSRF-Token': csrfToken || ''
                                    },
                                    credentials: 'same-origin'
                                });
                                if (resp.ok) {
                                    const prodData = await resp.json();
                                    preencherFormulario(prodData);
                                } else {
                                    preencherFormulario(produto);
                                }
                            } catch (err) {
                                preencherFormulario(produto);
                            }
                        });

                        formProdutos.appendChild(div);
                    });
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