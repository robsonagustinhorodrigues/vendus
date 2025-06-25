document.getElementById("formConsultaINPI").addEventListener("submit", function (e) {
  e.preventDefault();
  const termo = document.getElementById("termo").value;

  fetch("/dashboard/inpi/consulta", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ termo })
  })
    .then(res => res.json())
    .then(data => {
      const div = document.getElementById("resultadoINPI");
      div.innerHTML = "";

      if (data.status === "success") {
        data.resultados.forEach(r => {
          div.innerHTML += `
            <div class="card shadow-sm mb-3">
              <div class="card-body">
                <h5 class="card-title">${r.marca}</h5>
                <p class="card-text">Situação: <strong>${r.situacao}</strong></p>
                <p class="card-text">Processo: <code>${r.processo}</code></p>
              </div>
            </div>
          `;
        });
      } else {
        div.innerHTML = `<div class="alert alert-warning">${data.message}</div>`;
      }
    })
    .catch(err => {
      document.getElementById("resultadoINPI").innerHTML = `<div class="alert alert-danger">Erro: ${err}</div>`;
    });
});
