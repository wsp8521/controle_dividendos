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

// Atualiza a quantidade de ativos no módulo plano de metas
export function calculadora(elemento) {
    const metaId = elemento.getAttribute("data-meta-id");
    const campo = elemento.getAttribute("data-field");
    let novoValor = elemento.innerText.trim();

    // Captura a classe selecionada
    const tipoCalcInput = document.querySelector('input[name="tipo_calc"]:checked');
    const tipoCalc = tipoCalcInput?.value || null;

    console.log("classe selecionada:", tipoCalc);

    // Garantir formato numérico para proventos
    if (campo === "proventos") {
        novoValor = novoValor.replace(",", ".");
        if (isNaN(parseFloat(novoValor)) || novoValor === "") {
            novoValor = "0";
        }
    }

    const dados = { [campo]: novoValor };
    if (tipoCalc !== null) {
        dados['tipo_calc'] = tipoCalc;
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


function formatarReal(valor) {
    return valor.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}

export function calcularSaldo() {
    const valorInvestimentoSpan = document.getElementById("valor-investimento");
    const saldoSpan = document.getElementById("saldoAtual");
    const totais = document.querySelectorAll("td.total-ativo"); // Agora pega só os TOTAL de compra

    if (!valorInvestimentoSpan || !saldoSpan) return;

    let valorInvestido = parseFloat(valorInvestimentoSpan.innerText.replace("R$", "").replace(",", ".").trim()) || 0;
    let totalCompra = 0;

    totais.forEach(td => {
        let texto = td.innerText.replace("R$", "").replace(",", ".").trim();
        let valor = parseFloat(texto);
        if (!isNaN(valor)) {
            totalCompra += valor;
        }
    });

    let saldo = valorInvestido - totalCompra;
    saldoSpan.innerText = formatarReal(saldo);
}


export function recalcularTotalAtivo(cellQtd) {
    const linha = cellQtd.closest('tr');
    const qtdText = cellQtd.innerText.trim();
    const qtd = parseFloat(qtdText.replace(",", ".")) || 0;

    const cotacaoCell = linha.querySelector("td:nth-child(3)");
    const totalCell = linha.querySelector("td.total-ativo");

    if (!cotacaoCell || !totalCell) return;

    const cotacaoText = cotacaoCell.innerText.replace("R$", "").replace(",", ".").trim();
    const cotacao = parseFloat(cotacaoText) || 0;

    const novoTotal = qtd * cotacao;
    totalCell.innerText = formatarReal(novoTotal);
}


