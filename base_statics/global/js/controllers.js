// ======== Exibir ou ocultar o campo "Fonte de Recurso" no formulário de Operação ========

export function showInputFonteRecurso(){
    const campoOperacao = document.getElementById("id_tipo_operacao")
    const campoFonteRecurso = document.getElementById("id_fonte_recurso")
    const caixaFonte = campoFonteRecurso.closest(".mb-3");  // Pega a caixinha inteira onde está o campo "fonte de recurso"
    
   //incializa o estado do campo
    if(campoOperacao.value!="Venda"){
        caixaFonte.style.display="block"
    }else{
          caixaFonte.style.display="none"
    }

    campoOperacao.addEventListener('change', function(){
        if(this.value!="Venda"){
            caixaFonte.style.display="block"
        }else{
              caixaFonte.style.display="none"
        }  
    })  
}
