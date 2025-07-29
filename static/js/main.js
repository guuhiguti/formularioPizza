// Formatação do WhatsApp
document.getElementById("whatsapp").addEventListener("input", (e) => {
  let value = e.target.value.replace(/\D/g, "")
  if (value.length > 2) value = `(${value.slice(0, 2)}) ${value.slice(2)}`
  if (value.length > 10) value = `${value.slice(0, 10)}-${value.slice(10, 14)}`
  e.target.value = value
})
