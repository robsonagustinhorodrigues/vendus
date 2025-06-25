document.getElementById("formConsulta").addEventListener("submit", function (e) {
    e.preventDefault();

    const termo = document.getElementById("termo").value;
    const classe = document.getElementById("classe").value;
    const resultadosDiv = document.getElementById("resultados");
    resultadosDiv.innerHTML = '<div class="text-center">🔍 Buscando informações...</div>';

    fetch("/dashboard/inpi/consulta", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ termo: termo, classe: classe }),
    })
      .then((r) => r.json())
      .then((res) => {
        if (res.status === "success") {
          if (res.resultados.length === 0) {
            resultadosDiv.innerHTML =
              '<div class="alert alert-warning">Nenhum resultado encontrado.</div>';
            return;
          }

          resultadosDiv.innerHTML = res.resultados
            .map((item) => {
              return `
              <div class="col-md-6 col-lg-4">
                <div class="card border-0 shadow-sm h-100">
                  <div class="card-body">
                    <h5 class="card-title">${item.marca}</h5>
                    <p class="card-text small">
                      <strong>Classe:</strong> ${item.classe || 'N/D'}<br />
                      <strong>Tipo:</strong> ${item.tipo || 'N/D'}<br />
                      <strong>Registro:</strong> ${item.registro || 'N/D'}<br />
                      <strong>Processo:</strong> ${item.numero || 'N/D'}<br />
                      <strong>Situação:</strong> ${item.situacao || 'N/D'}<br />
                      <strong>Titular:</strong> ${item.titular || 'N/D'}<br />
                    </p>
                  </div>
                </div>
              </div>`;
            })
            .join("");
        } else {
          resultadosDiv.innerHTML = `<div class="alert alert-danger">Erro: ${res.message}</div>`;
        }
      })
      .catch((err) => {
        resultadosDiv.innerHTML = `<div class="alert alert-danger">Erro: ${err}</div>`;
      });
  });