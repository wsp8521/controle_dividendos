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
    var message = document.getElementById('successMessage');
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

    if (select.value != "Ação"){
        campoIpca.style.display = "block"
    } else{
        campoIpca.style.display = "none"
   }
}

//xxxxxxxxxxxxxxxxxxxxxxxxx Função para filtrar ativos com base na classe selecionada xxxxxxxxxxxxxxxxxxxxxx
    function filtrarAtivos(url) {
        const classeSelect = document.querySelector("select[name='classe']");  // Selecionando o select de classe
        const ativoSelect = document.querySelector("select[name='id_ativo']");  // Selecionando o select de ativos
        const classe = classeSelect.value;
        
        if (classe) {
            // Faz a requisição AJAX para filtrar os ativos
            fetch(`${url}/filtrar-ativos/?classe=${classe}`)
                .then(response => response.json())
                .then(data => {
                    // Limpa as opções de ativos
                    ativoSelect.innerHTML = '<option value="">Selecione um ativo...</option>';
                    
                    // Adiciona as opções recebidas da API
                    data.ativos.forEach(ativo => {
                        const option = document.createElement("option");
                        option.value = ativo.id;
                        option.textContent = ativo.nome;
                        ativoSelect.appendChild(option);
                    });
                })
                .catch(error => {
                    console.error("Erro ao buscar ativos:", error);
                });
        } else {
            // Se não houver classe selecionada, limpa o campo de ativos
            ativoSelect.innerHTML = '<option value="">Selecione uma classe primeiro...</option>';
        }
    }

    // Atribuindo a função filtrarAtivos ao evento onchange do select de classe
    document.addEventListener("DOMContentLoaded", () => {
        const classeSelect = document.querySelector("select[name='classe']");
        if (classeSelect) {
            classeSelect.addEventListener("change", function() {
                const url = "/preco/filtrar-ativos/";  // Aqui você pode passar uma URL diferente se necessário
                filtrarAtivos(url);  // Chama a função passando a URL
            });
        }
    });

