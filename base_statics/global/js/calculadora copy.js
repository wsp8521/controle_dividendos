let valorTabAtual = null; // Armazena o tipo da aba ativa (FII ou Ação)

export function calculadora() {
    // Inicializa o valor da aba ativa
    valorTabAtual = getClasseAbaAtiva();
    console.log("Aba ativa inicial:", valorTabAtual);

    // Captura todos os elementos editáveis da tabela
    capturarDadosTabela();

    // Atualiza tudo quando mudar de aba
    const tabs = document.querySelectorAll('#metaTabs button');
    tabs.forEach(tab => {
        tab.addEventListener('click', function () {
            setTimeout(() => {
                valorTabAtual = getClasseAbaAtiva();
                console.log("Aba ativa atualizada:", valorTabAtual);

                // Atualiza também os dados da tabela (se quiser recapturar)
                capturarDadosTabela();
            }, 100); // Espera a aba realmente ativar
        });
    });
}

// Função para pegar o valor da aba ativa
function getClasseAbaAtiva() {
    const tabAtiva = document.querySelector('#metaTabs .nav-link.active');
    if (tabAtiva) {
        return tabAtiva.getAttribute('data-field'); // FII ou Ação
    }
    return null;
}

// Função para capturar data-field e data-meta-id da tabela
function capturarDadosTabela() {
    const elementos = document.querySelectorAll('.editable-meta'); // Ou qualquer seletor dos campos editáveis
    elementos.forEach(elemento => {
        let campo = elemento.getAttribute('data-field');
        let metaId = elemento.getAttribute('data-meta-id');
        let valor = elemento.innerText.trim(); // Se quiser já pegar o valor preenchido

        console.log(`Aba ativa: ${valorTabAtual}, Campo: ${campo}, Meta ID: ${metaId}, Valor: ${valor}`);
    });
}

