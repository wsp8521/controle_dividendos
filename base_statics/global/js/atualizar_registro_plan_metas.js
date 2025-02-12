
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

// // xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxFunção para destacar a célula editadaxxxxxxxxxxxxxxxxxxxxxxxx
// function destacarCelula(elemento, tipo) {
//     elemento.style.backgroundColor = tipo === "success" ? "#d4edda" : "#f8d7da"; // Verde ou Vermelho

//     setTimeout(() => {
//         elemento.style.backgroundColor = ""; // Volta ao normal depois de 1,5s
//     }, 1500);
// }

//xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx Função para obter o CSRF Token do Django xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         let cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             let cookie = cookies[i].trim();
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }

// //xxxxxxxxxxxxxxxxxxxxxxxxxxx Função para exibir mensagem de sucesso/erro xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
// function exibirMensagem(mensagem, tipo) {
//     let mensagemDiv = document.createElement("div");
//     mensagemDiv.className = `alert ${tipo === "success" ? "alert-success" : "alert-danger"}`;
//     mensagemDiv.innerText = mensagem;

//     document.body.appendChild(mensagemDiv);

//     setTimeout(() => {
//         mensagemDiv.remove();
//     }, 3000); // Remove a mensagem após 3 segundos
// }

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

function atualizarMeta(elemento) {
     let metaId = elemento.getAttribute("data-meta-id");
     let novoValor = elemento.innerText.trim();
     let novo_valor_calc = elemento.innerText.trim();
     
     fetch(`/plan-metas/update/${metaId}`, {  // endpoint de para a atualização
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")  // Envia o CSRF token
        },
        body: JSON.stringify({
            "novo_valor": novoValor,
            "novo_valor_calc": novo_valor_calc
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            //exibirMensagem("Meta atualizada!");
            destacarCelula(elemento, "success"); // Destaca a célula alterada
            setTimeout(() => {location.reload();}, 1000);
            
            //exibirMensagem("Quantidade atualizada","success");
        } else {
            exibirMensagem("Erro ao atualizar: " + data.message);
        }
    })
    .catch(error => console.error("Erro:", error));
 }


//  // Função para atualizar apenas a tabela via AJAX
// function atualizarTabela() {
//     fetch("/plan-metas/atualizar-tabela")  // Endpoint que retorna a tabela renderizada
//     .then(response => response.text())
//     .then(html => {
//         document.querySelector(".table").innerHTML = html; // Substitui a tabela
//     })
//     .catch(error => console.error("Erro ao atualizar tabela:", error));
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
