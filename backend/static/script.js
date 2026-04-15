const API = "";

async function calcular() {
  const valor = parseFloat(document.getElementById("valor").value);
  const desconto = parseFloat(document.getElementById("desconto").value);
  const vip = document.getElementById("vip").checked;

  const res = await fetch(`${API}/calcular`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ valor, desconto, vip })
  });

  const data = await res.json();
  document.getElementById("resultado").innerText = `Cashback: R$ ${data.cashback}`;
  carregarHistorico();
}

async function carregarHistorico() {
  const res = await fetch(`${API}/historico`);
  const lista = await res.json();

  const ul = document.getElementById("historico");
  ul.innerHTML = "";

  lista.forEach(item => {
    const li = document.createElement("li");
    li.innerText = `${item[0]} | R$${item[1]} | Desc ${item[2]}% | Cashback R$${item[3]}`;
    ul.appendChild(li);
  });
}

carregarHistorico();