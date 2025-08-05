// Formatação do Número do WhatsApp
document.getElementById("whatsapp").addEventListener("input", (e) => {
  let value = e.target.value.replace(/\D/g, "")
  if (value.length > 2) value = `(${value.slice(0, 2)}) ${value.slice(2)}`
  if (value.length > 10) value = `${value.slice(0, 10)}-${value.slice(10, 14)}`
  e.target.value = value
})

// Função para calcular preço total progressivo (LÓGICA CORRIGIDA)
function calcularPrecoTotal(totalPizzas) {
  if (totalPizzas === 0) return 0

  const numPares = Math.floor(totalPizzas / 2)
  const restanteImpar = totalPizzas % 2

  const custo = numPares * 90 + restanteImpar * 50
  return custo
}

// Função para alterar quantidade de pizzas
function alterarQuantidade(sabor, delta) {
  const span = document.getElementById(`quantidade-${sabor}`)
  const input = document.getElementById(`input-${sabor}`)
  let atual = Number.parseInt(span.innerText)
  atual = Math.max(0, atual + delta)
  span.innerText = atual
  input.value = atual

  // Atualizar resumo
  atualizarResumo()
}

// Função para atualizar o resumo do pedido (SIMPLIFICADA)
function atualizarResumo() {
  const resumoPizzasDiv = document.getElementById("resumo-pizzas")
  const valorTotalSpan = document.getElementById("valor-total")
  const retiradaSelecionadaSpan = document.getElementById("retirada-selecionada")
  const detalhesRetiradaP = document.getElementById("detalhes-retirada")

  let pizzasHtml = ""
  let totalPizzasQuantidade = 0

  // Buscar todas as pizzas selecionadas
  const inputsPizzas = document.querySelectorAll('input[name^="pizza-"]')

  inputsPizzas.forEach((input) => {
    const quantidade = Number.parseInt(input.value)
    if (quantidade > 0) {
      const saborId = input.id.replace("input-", "")
      // Encontrar o nome da pizza a partir do ID (simulando o que o Flask faria)
      const pizzaNome = document
        .querySelector(`[id="quantidade-${saborId}"]`)
        .closest(".pizza-card")
        .querySelector("h4").textContent

      pizzasHtml += `<p>${pizzaNome}: ${quantidade}x</p>`
      totalPizzasQuantidade += quantidade
    }
  })

// RESUMO DO PEDIDO
  // Atualiza a lista de pizzas no resumo
  resumoPizzasDiv.innerHTML = pizzasHtml || "<p>Nenhuma pizza selecionada</p>"

  // Calcula e atualiza o valor total
  const valorTotal = calcularPrecoTotal(totalPizzasQuantidade)
  valorTotalSpan.textContent = valorTotal.toFixed(2).replace(".", ",")

  // Atualiza a informação de retirada
  const radioRetirada = document.querySelector('input[name="retirada"]:checked')
  let textoRetirada = "Selecione uma opção"
  let detalhes = ""

  if (radioRetirada) {
    if (radioRetirada.value === "arena") {
      textoRetirada = "Arena Bonfim"
      const radioDiaRetirada = document.querySelector('input[name="dia_retirada"]:checked')
      if (radioDiaRetirada) {
        const diasMap = {
          quinta: "Quinta-feira, 11/09 das 17h às 21h",
          sexta: "Sexta-feira, 12/09 das 16h às 20h",
          sabado: "Sábado, 13/09 das 9h às 14h",
        }
        detalhes = diasMap[radioDiaRetirada.value]
      }
    } else if (radioRetirada.value === "voluntario") {
      textoRetirada = "Com Voluntário do Ser Solidário"
      const nomeVoluntarioInput = document.getElementById("nome_voluntario")
      if (nomeVoluntarioInput && nomeVoluntarioInput.value) {
        detalhes = `Voluntário: ${nomeVoluntarioInput.value}`
      }
    } else if (radioRetirada.value === "doacao") {
      textoRetirada = "Doação para Famílias Carentes"
    }
  }
  retiradaSelecionadaSpan.textContent = textoRetirada
  detalhesRetiradaP.textContent = detalhes
}



// Event Listeners para as opções de retirada
const radiosRetirada = document.getElementsByName("retirada")
const blocoArena = document.getElementById("arena")
const blocoVoluntario = document.getElementById("voluntario")
const radiosDiaRetirada = document.getElementsByName("dia_retirada")
const inputNomeVoluntario = document.getElementById("nome_voluntario")

radiosRetirada.forEach((radio) => {
  radio.addEventListener("change", () => {
    // Esconde todos os blocos extras primeiro
    blocoArena.style.display = "none"
    blocoVoluntario.style.display = "none"

    // Remove 'required' de todos os campos extras
    radiosDiaRetirada.forEach((r) => (r.required = false))
    if (inputNomeVoluntario) inputNomeVoluntario.required = false

    // Mostra o bloco correspondente e define 'required'
    if (radio.value === "arena") {
      blocoArena.style.display = "block"
      radiosDiaRetirada.forEach((r) => (r.required = true))
    } else if (radio.value === "voluntario") {
      blocoVoluntario.style.display = "block"
      if (inputNomeVoluntario) inputNomeVoluntario.required = true
    }
    atualizarResumo() // Atualiza o resumo ao mudar a opção de retirada
  })
})

// Listener para os radios de dia de retirada (se Arena Bonfim for selecionado)
radiosDiaRetirada.forEach((radio) => {
  radio.addEventListener("change", atualizarResumo)
})

// Listener para o input do nome do voluntário
if (inputNomeVoluntario) {
  inputNomeVoluntario.addEventListener("input", atualizarResumo)
}

// Atualizar resumo quando a página carregar
document.addEventListener("DOMContentLoaded", () => {
  const pizzaForm = document.getElementById("pizza-form")
  const pizzaSelectionErrorDiv = document.getElementById("pizza-selection-error")

  pizzaForm.addEventListener("submit", function (event) {
    // Previne o envio padrão do formulário para fazer a validação personalizada
    event.preventDefault()

    // PASSO 1: Verificar validações HTML5 (incluindo 'required')
    // Se o formulário não for válido (algum campo 'required' está vazio, etc.),
    // o navegador exibirá as mensagens de erro nativas e esta função retornará.
    if (!this.checkValidity()) {
      // Opcional: Esconder a mensagem de erro de pizza se ela estiver visível
      pizzaSelectionErrorDiv.style.display = "none"
      return // Impede o envio do formulário
    }

    // PASSO 2: Validação personalizada para a seleção de pizzas
    let totalPizzasQuantidade = 0
    const inputsPizzas = document.querySelectorAll('input[name^="pizza-"]')
    inputsPizzas.forEach((input) => {
      totalPizzasQuantidade += Number.parseInt(input.value)
    })

    // Validação: Pelo menos uma pizza deve ser selecionada
    if (totalPizzasQuantidade === 0) {
      pizzaSelectionErrorDiv.style.display = "block" // Mostra a mensagem de erro
      // Opcional: rolar para a seção de pizzas
      document.getElementById("pizza-container").scrollIntoView({ behavior: "smooth", block: "center" })
      return // Impede o envio do formulário
    } else {
      pizzaSelectionErrorDiv.style.display = "none" // Esconde a mensagem de erro se houver pizzas
    }

    // PASSO 3: Se todas as validações do cliente passarem, permite o envio do formulário
    this.submit()
  })

  // Certifique-se de que o resumo é atualizado ao carregar a página
  atualizarResumo()
})
