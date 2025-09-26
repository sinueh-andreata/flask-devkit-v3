// csrf-handler.js
// Script para buscar o CSRF token e inserir automaticamente nos formulários

document.addEventListener('DOMContentLoaded', function() {
    // Função para buscar o CSRF token
    async function fetchCSRFToken() {
        try {
            const response = await fetch('/csrf-token', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                return data.csrf_token;
            } else {
                console.error('Erro ao buscar CSRF token:', response.status);
                return null;
            }
        } catch (error) {
            console.error('Erro na requisição do CSRF token:', error);
            return null;
        }
    }

    // Função para inserir o CSRF token em todos os formulários
    async function insertCSRFToken() {
        const token = await fetchCSRFToken();
        
        if (token) {
            // Encontra todos os campos CSRF token nos formulários
            const csrfInputs = document.querySelectorAll('input[name="csrf_token"]');
            
            csrfInputs.forEach(function(input) {
                input.value = token;
            });
            
            console.log('CSRF token inserido em', csrfInputs.length, 'formulários');
        } else {
            console.error('Não foi possível obter o CSRF token');
        }
    }

    // Executa a inserção do CSRF token quando a página carrega
    insertCSRFToken();
});