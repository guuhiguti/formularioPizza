// Formatação do Número do WhatsApp




// Botões das Pizzas
function alterarQuantidade(sabor, delta) {
    const span = document.getElementById(`quantidade-${sabor.replaceAll(' ', '-')}`);
    const input = document.getElementById(`input-${sabor.replaceAll(' ', '-')}`);

    let atual = parseInt(span.innerText);
    atual = Math.max(0, atual + delta);

    span.innerText = atual;
    input.value = atual;
}




// Perguntas Dinâmicas de Acordo com a Opção Selecionada
const radios = document.getElementsByName('retirada');
const blocoArena = document.getElementById('arena');
const blocoVoluntario = document.getElementById('voluntario');

const radiosRetirada = document.getElementsByName('dia_retirada');
const inputVoluntario = document.querySelector('input[name="nome_voluntario"]');

radios.forEach(radio => {
    radio.addEventListener('change', () => {
        if (radio.value === 'arena') {
            blocoArena.style.display = 'block';
            blocoVoluntario.style.display = 'none';
            radiosRetirada.forEach(r => r.required = true);
            inputVoluntario.required = false;

        } else if (radio.value === 'voluntario') {
            blocoArena.style.display = 'none';
            blocoVoluntario.style.display = 'block'
            radiosRetirada.forEach(r => r.required = false);
            inputVoluntario.required = true;

        } else {
            blocoArena.style.display = 'none';
            blocoVoluntario.style.display = 'none'
            radiosRetirada.forEach(r => r.required = false);
            inputVoluntario.required = false;
        }
    });
});