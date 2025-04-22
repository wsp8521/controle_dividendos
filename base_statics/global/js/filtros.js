   // ========= FILTRAR SETOR POR CLASSE - FORM CADASTRO DE ATIVO =======
   // filtros.js
   export function FiltrarSetor() {
    const classeField = document.getElementById("id-classe");
    const setorField = document.getElementById("id-setor");

        classeField.addEventListener("change", function () {
            
            const selectedClasse = this.value
            if (selectedClasse!="False"){ //verifica se foi selecionado uma opção
                setorField.disabled = false
                 fetch(`/get-setores/?classe=${selectedClasse}`)
                    .then(response => response.json())
                    .then(data => {
                        // Limpa as opções atuais
                        setorField.innerHTML = '<option value="">---</option>';
                        data.forEach(item => {
                            const option = document.createElement("option");
                            option.value = item.id;
                            option.textContent = item.setor;
                            setorField.appendChild(option);
                        });
                    });
            }else{
                setorField.disabled = true 
            }
        })
}

//xxxxxxxxxxxxxxxxxxxxxxxxx Função para filtrar ativos com base na classe selecionada xxxxxxxxxxxxxxxxxxxxxx
export function filtrarAtivos(url) {
    const classeSelect = document.querySelector("select[name='classe']");  // Selecionando o select de classe
    const ativoSelect = document.querySelector("select[name='id_ativo']");  // Selecionando o select de ativos
   
    classeSelect.addEventListener("change", function () {
    const classe = this.value; // Aqui pega o valor atualizado

    if(classe!="False"){
        //     // Faz a requisição AJAX para filtrar os ativos
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



    }else{
        // Se não houver classe selecionada, limpa o campo de ativos
        ativoSelect.innerHTML = '<option value="">Selecione uma classe primeiro...</option>';
    }
})
}

// ========= FILTRAR STATUS - PÁGINA AGENDA NA TABELA FII PENDENTE =======
export function filtrarStatus(selectElement) {
    const url = new URL(window.location.href);
    url.searchParams.set('filtro_status', selectElement.value);
    window.history.replaceState({}, '', url); // Atualiza a URL sem reload
  
    fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
      .then(response => response.text())
      .then(html => {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const novaTabela = doc.querySelector('#pgto-pendente');
        if (novaTabela) {
          document.querySelector('#pgto-pendente').innerHTML = novaTabela.innerHTML;
        }
      });
  }
  