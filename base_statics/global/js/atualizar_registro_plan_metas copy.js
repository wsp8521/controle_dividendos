
//xxxxxxxxxxxxxxxxxxxxxxxxxxx Função para exibir mensagem de sucesso/erro xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
function exibirMensagem(mensagem, tipo) {
    let mensagemDiv = document.createElement("div");
    mensagemDiv.className = `alert ${tipo === "success" ? "alert-success" : "alert-danger"}`;
    mensagemDiv.innerText = mensagem;

    document.body.appendChild(mensagemDiv);

    setTimeout(() => {
        mensagemDiv.remove();
    }, 3000); // Remove a mensagem após 3 segundos
}

// xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx xxxFunção para destacar a célula editadaxxxxxxxxxxxxxxxxxxxxxxxx
function destacarCelula(elemento, tipo) {
    elemento.style.backgroundColor = tipo === "success" ? "#025614" : "#f8d7da"; // Verde ou Vermelho

    setTimeout(() => {
        elemento.style.backgroundColor = ""; // Volta ao normal depois de 1,5s
    }, 1500);
}



/***********************************************************
 ************** FUNÇÕES DE ATUALIZAÇÃO *********************
***********************************************************/

document.addEventListener("DOMContentLoaded", function() {
    let cells = document.querySelectorAll("[contenteditable=true]");

    cells.forEach(cell => {
        let valorOriginal = cell.innerText.trim(); // Guarda o valor antes da edição

        cell.addEventListener("keypress", function(event) {
            if (event.keyCode === 13) {  // Se pressionar Enter
                event.preventDefault(); // Impede quebra de linha
                if (this.innerText.trim() !== valorOriginal) {
                    atualizarMeta(this);

                    // Atualiza o TOTAL PROV em tempo real se for campo relevante
                    let campo = this.getAttribute("data-field");
                    if (campo === "qtd_calc" || campo === "proventos") {
                        let metaId = this.getAttribute("data-meta-id");
                        atualziarTotais(metaId);
                    }
                }
            }
        });

        // (Opcional) Se quiser atualizar também ao perder foco, descomente:
        // cell.addEventListener("blur", function() {
        //     if (this.innerText.trim() !== valorOriginal) {
        //         atualizarMeta(this);
        //         let campo = this.getAttribute("data-field");
        //         if (campo === "qtd_calc" || campo === "proventos") {
        //             let metaId = this.getAttribute("data-meta-id");
        //             atualizarTotalProvento(metaId);
        //         }
        //     }
        // });
    });
});

// Atualiza a quantidade de ativos no módulo plano de metas
function atualizarMeta(elemento) {
    let metaId = elemento.getAttribute("data-meta-id");
    let campo = elemento.getAttribute("data-field");
    let novoValor = elemento.innerText.trim();  

    // Tentar capturar o tipo_calc apenas se existir o input
    let tipoCalcInput = document.querySelector('input[name="tipo_calc"]:checked');
    let tipoCalc = tipoCalcInput ? tipoCalcInput.value : null;  // Se não existir, deixa null ou outro valor padrão

    // Se for a coluna de proventos, garantir que está no formato correto
    if (campo === "proventos") {
        novoValor = novoValor.replace(",", ".");  // Substitui vírgula por ponto
        if (isNaN(novoValor) || novoValor === "") {
            novoValor = "0";  // Evita erro ao enviar string vazia
        }
    }

    let dados = {};
    dados[campo] = novoValor; 

    if (tipoCalc !== null) {  
        dados['tipo_calc'] = tipoCalc;  // Só adiciona se existir
    }

    // Montando a URL para o fetch
    let url;
    if (campo === "valor_investimento" && isNaN(metaId)) {
        url = `/plan-metas/calculadora/investimento/`;
    } else {
        url = (campo === "valor_investimento" && !isNaN(metaId)) 
            ? `/plan-metas/calculadora/${metaId}` 
            : `/plan-metas/update/${metaId}`;
    }
 
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify(dados)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            destacarCelula(elemento, "success");
        } else {
            exibirMensagem("Erro ao atualizar: " + data.message);
        }
    })
    .catch(error => console.error("Erro:", error));
}

function atualizarTotais(metaId) {
    // Atualizar TOTAL PROV da linha
    let qtdSpan = document.querySelector(`span[data-meta-id="${metaId}"][data-field="qtd_calc"]`);
    let provSpan = document.querySelector(`span[data-meta-id="${metaId}"][data-field="proventos"]`);
    let totalProvCell = qtdSpan.closest('tr').querySelectorAll('.prov-col')[1]; // Segunda célula prov-col da linha (TOTAL PROV)

    if (qtdSpan && provSpan && totalProvCell) {
        let qtd = parseFloat(qtdSpan.innerText.replace(",", "."));
        let provento = parseFloat(provSpan.innerText.replace(",", "."));

        if (isNaN(qtd)) qtd = 0;
        if (isNaN(provento)) provento = 0;

        let totalProvento = qtd * provento;

        let totalFormatado = totalProvento.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });

        totalProvCell.textContent = totalFormatado;
    }

    // Atualizar TOTAL DINHEIRO e SALDO
    let totalDinheiro = 0;
    let linhas = document.querySelectorAll("table tbody tr");

    linhas.forEach(linha => {
        let qtdSpanLinha = linha.querySelector('span[data-field="qtd_calc"]');
        let cotacaoCell = linha.querySelectorAll('td')[2]; // 3ª coluna é COTAÇÃO

        if (qtdSpanLinha && cotacaoCell) {
            let qtdLinha = parseFloat(qtdSpanLinha.innerText.replace(",", "."));
            let cotacaoText = cotacaoCell.innerText.replace("R$", "").replace(",", ".").trim();
            let cotacao = parseFloat(cotacaoText);

            if (isNaN(qtdLinha)) qtdLinha = 0;
            if (isNaN(cotacao)) cotacao = 0;

            let totalLinha = qtdLinha * cotacao;

            // Atualizar o TOTAL de cada linha (coluna TOTAL)
            let totalCell = linha.querySelectorAll('td')[3]; // 4ª coluna é TOTAL
            if (totalCell) {
                let totalLinhaFormatado = totalLinha.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
                totalCell.textContent = totalLinhaFormatado;
            }

            totalDinheiro += totalLinha;
        }
    });

    // Atualizar TOTAL GERAL na linha de rodapé
    let tdTotalDinheiro = document.querySelector("table tbody tr.fw-bold td:nth-child(4)");
    if (tdTotalDinheiro) {
        let totalDinheiroFormatado = totalDinheiro.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
        tdTotalDinheiro.textContent = totalDinheiroFormatado;
    }

    // Atualizar SALDO (valor investimento - totalDinheiro)
    let valorInvestimentoSpan = document.getElementById("valor-investimento");
    if (valorInvestimentoSpan) {
        let valorInvestimentoText = valorInvestimentoSpan.innerText.replace("R$", "").replace(",", ".").trim();
        let valorInvestimento = parseFloat(valorInvestimentoText);

        if (isNaN(valorInvestimento)) valorInvestimento = 0;

        let saldo = valorInvestimento - totalDinheiro;
        let saldoFormatado = saldo.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });

        let saldoTh = document.querySelector("table thead tr:first-child th:last-child");
        if (saldoTh) {
            saldoTh.innerHTML = `SALDO ${saldoFormatado}`;
        }
    }
}


// Função para obter o CSRF Token do Django
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
