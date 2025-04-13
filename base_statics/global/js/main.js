import { FiltrarSetor, filtrarAtivos } from './filtros.js';
import { showInputFonteRecurso } from './controllers.js';


/**AÇOES NOS FORMULÁIROS DO MODAL */
document.body.addEventListener('htmx:afterSwap', (event) => {
   
    // Executa apenas se o conteúdo veio para o modal
    if (event.target.id === 'addContent' || event.target.id === 'addContentSetor') {

        // Chama FiltrarSetor somente se os campos existirem
        if (document.getElementById("id-classe") && document.getElementById("id-setor")) {
            FiltrarSetor();
        }

        // Chama filtrarAtivos somente se os campos existirem
        if (document.querySelector("select[name='classe']") && document.querySelector("select[name='id_ativo']")) {
            /*pegado o link de forma dinamica*/
            const form = document.querySelector("form[data-url]");
            const url = form.getAttribute("data-url")
            filtrarAtivos(url); // passe a URL correta se precisar
        }


           // Executa a função para exibir/ocultar o campo Fonte de Recurso
           if (document.getElementById("id_fonte_recurso")) {
            showInputFonteRecurso();
        }
    }
});

/**PERSISTENCIA DE DADOS - FORM ADICONAR ATIVO  */
