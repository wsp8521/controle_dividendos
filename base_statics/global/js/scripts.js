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
  

  //função para esconder mensagem de sucesso
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

  

