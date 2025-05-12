export function salvarDadosFormularioAtivo() {
    const form = document.querySelector('#cadastroModal form');
    const dados = {};
    if (form) {
        [...form.elements].forEach(el => {
            if (el.name && el.type !== 'submit' && el.type !== 'button') {
                dados[el.name] = el.value;
            }
        });
    }
    sessionStorage.setItem('formulario_ativo_cache', JSON.stringify(dados));
}




document.addEventListener('DOMContentLoaded', function () {
    const dadosSalvos = sessionStorage.getItem('formulario_ativo_cache');
    if (dadosSalvos) {
        const dados = JSON.parse(dadosSalvos);
        const form = document.querySelector('#cadastroModal form');
        if (form) {
            Object.entries(dados).forEach(([name, value]) => {
                const field = form.querySelector(`[name="${name}"]`);
                if (field) {
                    field.value = value;
                }
            });
        }
    }
});