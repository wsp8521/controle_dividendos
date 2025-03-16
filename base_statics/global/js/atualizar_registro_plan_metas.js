
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


//xxxxxxxxxxxxxxxxxxxxxxxxx Função para atulzar dados na celula da tabela xxxxxxxxxxxxxxxxxxxxxx
document.addEventListener("DOMContentLoaded", function() {
    let cells = document.querySelectorAll("[contenteditable=true]");

    cells.forEach(cell => {
        cell.addEventListener("keypress", function(event) {
            if (event.keyCode === 13) {  // Tecla Enter
                event.preventDefault(); // Impede que pule uma linha dentro da célula
                atualizarMeta(this);
            }
        });
    });
});
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
                    //atualizarValorInvestimento(this)
                }
            }
        });

        cell.addEventListener("blur", function() {  // Se clicar fora
            if (this.innerText.trim() !== valorOriginal) {
                atualizarMeta(this);
                //atualizarValorInvestimento(this)
            }
        });
    });
});

//atualiza a quantidade de ativos no modulo plano de meatas
function atualizarMeta(elemento) {
    let metaId = elemento.getAttribute("data-meta-id");
    let campo = elemento.getAttribute("data-field");
    let novoValor = elemento.innerText.trim();  

    console.log("campo: "+campo)

    // Se for a coluna de proventos, garantir que está no formato correto
    if (campo === "proventos") {
        novoValor = novoValor.replace(",", ".");  // Substitui vírgula por ponto
        if (isNaN(novoValor) || novoValor === "") {
            novoValor = "0";  // Evita erro ao enviar string vazia
        }
    }

    let dados = {};
    dados[campo] = novoValor; 

    url = campo === "valor_investimento" ? `/plan-metas/calculadora/${metaId}` : `/plan-metas/update/${metaId}`;

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
            setTimeout(() => { location.reload(); }, 1000);
        } else {
            exibirMensagem("Erro ao atualizar: " + data.message);
        }
    })
    .catch(error => console.error("Erro:", error));
}

// //atualiza o valor do investsimento no modulo calculadora
// function atualizarValorInvestimento(elemento) {
//     let metaId = elemento.getAttribute("data-meta-id");
//     let campo = elemento.getAttribute("data-field");
//     let novoValor = elemento.innerText.trim();  

//     // Se for a coluna de proventos, garantir que está no formato correto
//     if (campo === "valor_investimento") {
//         novoValor = novoValor.replace(",", ".");  // Substitui vírgula por ponto
//         if (isNaN(novoValor) || novoValor === "") {
//             novoValor = "0";  // Evita erro ao enviar string vazia
//         }
//     }

//     let dados = {};
//     dados[campo] = novoValor;  

//     fetch(`/plan-metas/calculadora/${metaId}`, {
//         method: "POST",
//         headers: {
//             "Content-Type": "application/json",
//             "X-CSRFToken": getCookie("csrftoken")
//         },
//         body: JSON.stringify(dados)
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.status === "success") {
//             destacarCelula(elemento, "success");
//             setTimeout(() => { location.reload(); }, 1000);
//         } else {
//             exibirMensagem("Erro ao atualizar: " + data.message);
//         }
//     })
//     .catch(error => console.error("Erro:", error));
// }



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
