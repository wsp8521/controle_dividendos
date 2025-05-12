//Função que aciona a modal de deleção de registros
function modal(element){
    new bootstrap.Modal("#modalDel").show(); //acionando a modal
    var name = element.getAttribute('data-name');
    var page = element.getAttribute('data-page');
    var id = element.getAttribute('data-id'); //pegando os dados passado pelo atributo data-id
    var modalBodyContent = document.getElementById('modalBodyContent'); //elemento que rá receber a mensagem
    var deleteForm = document.getElementById('deleteForm');
   modalBodyContent.textContent = 'Tem certeza que deseja excluir o registro '+ name + '?'; //inserindo mensagem na modal
   deleteForm.action = '/'+page+'/delete/' + id ; //aciona o link de exclusão da 
    }
  
  //xxxxxxxxxxxxxxxxxxxxxxxfunção para esconder mensagem de sucesso xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

  function showAndHideSuccessMessage(showTimeout = 0, hideTimeout = 1000) {
    var message = document.getElementById('msgAlert');
    if (message) {
        // Mostrar a mensagem após um tempo (útil para dar tempo ao DOM de carregar)
        setTimeout(function() {
            message.classList.add('visible');  // Adiciona a classe que mostra a mensagem
  
            // Esconder a mensagem após o tempo definido
            setTimeout(function() {
                message.classList.remove('visible');
                message.classList.add('hidden');  // Adiciona a classe que esconde a mensagem
  
                // Remover o elemento após a transição de ocultar
                setTimeout(function() {
                    message.style.display = 'none';  // Esconde o elemento após a transição
                }, 500);  // Duração da transição de ocultar (0.5 segundos)
            }, hideTimeout);  // Tempo antes de iniciar o desaparecimento
        }, showTimeout);  // Tempo antes de mostrar a mensagem (normalmente 0)
    }
  }

//xxxxxxxxxxxxxxxxxxxxx ocultar campo IPCA do formulário da pagina preço teto xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

function hiddenCampoIpca() {
    let select = document.getElementById("id_classe");
    let campoIpca = document.getElementById("container_ipca");

    if (select.value === "Ação"){
        campoIpca.style.display = "none"
    } else{
        campoIpca.style.display = "block"
   }
}

    // //xxxxxxxxxxxxxxxxxxxxxxxxx PopUp de pesquisa de proventos xxxxxxxxxxxxxxxxxxxxxx

// Função para iniciar a pesquisa
function iniciarPesquisa() {
    const btn = document.getElementById("iniciarPesquisaBtn");
    const url = btn.getAttribute("data-url");  // Obtém a URL do atributo data-url

    // Mostra o pop-up de carregando
    const loadingPopup = document.createElement("div");
    loadingPopup.id = "loadingPopup";
    loadingPopup.style.position = "fixed";
    loadingPopup.style.top = "50%";
    loadingPopup.style.left = "50%";
    loadingPopup.style.transform = "translate(-50%, -50%)";
    loadingPopup.style.padding = "20px";
    loadingPopup.style.backgroundColor = "blue";
    loadingPopup.style.color = "white";
    loadingPopup.style.border = "1px solid black";
    loadingPopup.style.zIndex = "1000";
    loadingPopup.innerText = "Pesquisando datas de pagamento da Web. Por favor aguarde...";
    document.body.appendChild(loadingPopup);

    // Faz a requisição para iniciar a tarefa Celery
    fetch(url, {
        method: "GET",
        headers: {
            "X-Requested-With": "XMLHttpRequest"
        }
    })
    .then(response => response.json())
    .then(data => {
        const taskId = data.task_id;
        verificarStatusTarefa(taskId);
    })
    .catch(error => {
        console.error("Erro ao iniciar a tarefa:", error);
        document.body.removeChild(loadingPopup);
        alert("Erro ao iniciar a pesquisa.");
    });
}

// Função para verificar o status da tarefa Celery
function verificarStatusTarefa(taskId) {
    const interval = setInterval(() => {
        fetch(`/status-tarefa/${taskId}/`, {
            method: "GET",
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "SUCCESS") {
                clearInterval(interval);
                document.body.removeChild(document.getElementById("loadingPopup"));
                
                // Exibe mensagem com o número de registros cadastrados
                alert(data.result);  

                location.reload();  // Atualiza a página
            } else if (data.status === "FAILURE") {
                clearInterval(interval);
                document.body.removeChild(document.getElementById("loadingPopup"));
                alert("❌ Erro ao executar a tarefa.");
            }
        })
        .catch(error => {
            clearInterval(interval);
            document.body.removeChild(document.getElementById("loadingPopup"));
            alert("Erro ao verificar o status da tarefa.");
        });
    }, 2000);
}

// Adiciona o event listener para o botão
document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("iniciarPesquisaBtn");
    if (btn) {
        btn.addEventListener("click", iniciarPesquisa);
    }
});


//ATUALIZAÇAO DE COTAÇÕES
document.addEventListener("DOMContentLoaded", function() {
    let btn = document.getElementById("atualizarCotacaoBtn");
    
    if (btn) {
        btn.addEventListener("click", function(event) {
            event.preventDefault(); // Evita que o botão siga o link

            fetch("/ativo/atualizar-cotacao/")
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    let msgDiv = document.getElementById("successMessageCotacao");

                    if (msgDiv) {
                        msgDiv.innerText = data.mensagem;
                        msgDiv.style.display = "block"; // Exibe a mensagem
                    }

                    // Aguarda 3 segundos antes de recarregar a página
                    setTimeout(() => {
                        location.reload();
                    }, 3000);
                }
            })
            .catch(error => console.error("Erro ao atualizar cotações:", error));
        });
    } 
});

