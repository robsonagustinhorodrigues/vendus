document.getElementById("formRanqueamento").addEventListener("submit", function (e) {
  e.preventDefault();
  const form = e.target;
  const termo = document.getElementById("termoBusca").value.trim();
  const integracaoId = document.getElementById("integracaoSelect").value;
  const resultado = document.getElementById("resultadoRanqueamento");
  const erro = document.getElementById("mensagemErro");

  resultado.innerHTML = "<p>Buscando posições...</p>";
  erro.classList.add("d-none");

  fetch("/dashboard/meli_ranqueamento/buscar", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ termo, integracao_id: integracaoId })
  })
    .then((r) => r.json())
    .then((data) => {
      resultado.innerHTML = "";
      if (data.status !== "success") {
        erro.textContent = data.message || "Erro ao buscar posições.";
        erro.classList.remove("d-none");
        return;
      }

      if (!data.data || Object.keys(data.data).length === 0) {
        resultado.innerHTML = "<p class='text-center text-muted'>Nenhum anúncio encontrado nas 20 primeiras páginas.</p>";
        return;
      }

      const table = document.createElement("table");
      table.className = "table table-bordered table-sm table-hover mt-3";
      table.innerHTML = `
        <thead class="table-light">
          <tr>
            <th>MLB</th>
            <th>Página</th>
            <th>Posição na Página</th>
            <th>Posição Global</th>
            <th>Link</th>
          </tr>
        </thead>
        <tbody>
          ${Object.entries(data.data).map(([mlb, info]) => `
            <tr>
              <td>${mlb}</td>
              <td>${info.pagina}</td>
              <td>${info.posicao_na_pagina}</td>
              <td>${info.posicao_total}</td>
              <td><a href="${info.url}" target="_blank">Ver Anúncio</a></td>
            </tr>`).join("")}
        </tbody>
      `;

      resultado.appendChild(table);
    })
    .catch(() => {
      resultado.innerHTML = "";
      erro.textContent = "Erro ao buscar posição dos anúncios.";
      erro.classList.remove("d-none");
    });
});