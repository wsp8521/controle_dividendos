import { FiltrarSetor, filtrarAtivos, filtrarStatus } from './filtros.js';
import { showInputFonteRecurso } from './controllers.js';
import { calculadora, calcularSaldo, recalcularTotalAtivo } from './calculadora.js';

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

    // // Executa a função de atualização de dados na calculadora da pagina plano de metas
    if (event.target.id === 'ModalGeralContent') {
        let cells = document.querySelectorAll("[contenteditable=true]");

        cells.forEach(cell => {
            let valorOriginal = cell.innerText.trim();

            cell.addEventListener("keypress", function (event) {
                if (event.keyCode === 13) {  // Se pressionar Enter
                    event.preventDefault();
                    if (this.innerText.trim() !== valorOriginal) {
                        calculadora(this);

                        let campo = this.getAttribute("data-field");
                        let metaId = this.getAttribute("data-meta-id");
                        // Atualizar saldo ao editar o valor investido
                        const valorInvestimentoSpan = document.getElementById("valor-investimento");
                        if (valorInvestimentoSpan) {
                            valorInvestimentoSpan.addEventListener("input", calcularSaldo);
                        }

                        // Atualizar saldo ao editar quantidade de ativos
                        const cellsEditable = document.querySelectorAll("[data-field='qtd_calc']");
                        cellsEditable.forEach(cell => {
                            cell.addEventListener("input", function () {
                                calcularSaldo();
                                recalcularTotalAtivo(this)
                            });
                        });

                    }
                }
            });
        });
    }
});



//FILTRAR STATUS
document.addEventListener("DOMContentLoaded", function () {
    const filtroStatus = document.getElementById("filtro_ativo");

    if (filtroStatus) {
        filtroStatus.addEventListener("change", function () {
            filtrarStatus(this);
        });
    }
});