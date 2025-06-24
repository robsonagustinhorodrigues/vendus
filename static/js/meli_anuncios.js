document
  .getElementById("formBuscaAnuncios")
  .addEventListener("submit", function (e) {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);
    const resultado = document.getElementById("resultadoBusca");
    const erro = document.getElementById("mensagemErro");
    const integracaoId = document.getElementById("integracaoSelect").value;

    resultado.innerHTML = "<p>Carregando...</p>";
    erro.classList.add("d-none");

    fetch("/dashboard/meli_anuncios/buscar", {
      method: "POST",
      body: formData,
    })
      .then((res) => res.json())
      .then((data) => {
        resultado.innerHTML = "";
        if (data.status === "success") {
          const ids = data.data.results;
          if (!ids.length) {
            resultado.innerHTML =
              "<p class='text-center text-muted'>Nenhum anúncio encontrado.</p>";
            return;
          }

          fetch(
            `/api/meli/items?integracao_id=${integracaoId}&ids=${ids.join()}`
          )
            .then((r) => r.json())
            .then((resposta) => {
              if (
                resposta.status !== "success" ||
                !resposta.data ||
                !Array.isArray(resposta.data)
              ) {
                throw new Error("Formato inesperado na resposta da API.");
              }

              resposta.data.forEach((obj) => {
                const anuncio = obj.body;
                const col = document.createElement("div");
                col.className = "col-md-4";
                const link = `https://produto.mercadolivre.com.br/${anuncio.id}`;
                const jsonStr = encodeURIComponent(JSON.stringify(anuncio));
                col.innerHTML = `
                    <div class="card shadow-sm border-0 h-100">
                    <img src="${anuncio.thumbnail}" class="card-img-top" alt="${
                  anuncio.title
                }" style="height: 250px; object-fit: cover;">
                    <div class="card-body">
                        <h6 class="card-title fw-bold">
                        ${anuncio.title}
                        <i class="bi bi-clipboard text-secondary me-1" role="button" onclick="copiarTexto('${
                          anuncio.title
                        }')"></i>
                        </h6>
                        <p class="mb-1 small text-muted">
                        <strong>MLB:</strong> ${anuncio.id}
                        <i class="bi bi-clipboard ms-1 text-secondary" role="button" onclick="copiarTexto('${
                          anuncio.id
                        }')"></i>
                        </p>
                        <p class="mb-1 small text-muted">
                        <strong>Link:</strong> 
                        <a href="${link}" target="_blank">Ver Anúncio</a>
                        <i class="bi bi-clipboard ms-1 text-secondary" role="button" onclick="copiarTexto('${link}')"></i>
                        </p>
                        <p class="mb-1">
                        <strong>Preço:</strong> R$ ${anuncio.price.toFixed(2)}
                        </p>
                        <p class="mb-1"><strong>Status:</strong> ${
                          anuncio.status
                        }</p>
                        <p class="mb-1"><strong>Estoque:</strong> ${
                          anuncio.available_quantity
                        }</p>
                        <p class="mb-2 text-muted small"><strong>Categoria:</strong> ${
                          anuncio.category_id
                        }</p>
                        <button class="btn btn-sm btn-outline-dark w-100 mb-2" 
                                data-json="${jsonStr}" 
                                onclick="mostrarJsonModal(this)">
                            <i class="bi bi-code-slash me-1"></i> Mostrar JSON
                        </button>
                        <pre class="d-none small p-2 bg-light rounded border mt-2">${JSON.stringify(
                          anuncio,
                          null,
                          2
                        )}</pre>
                    </div>
                    </div>
                `;
                resultado.appendChild(col);
              });
            })
            .catch((e) => {
              erro.textContent = "Erro ao buscar detalhes dos anúncios.";
              erro.classList.remove("d-none");
            });
        } else {
          erro.textContent = data.message || "Erro ao buscar anúncios.";
          erro.classList.remove("d-none");
        }
      })
      .catch(() => {
        resultado.innerHTML = "";
        erro.textContent = "Erro na requisição.";
        erro.classList.remove("d-none");
      });
  });

function copiarTexto(texto) {
  navigator.clipboard.writeText(texto).then(() => {
    const toast = document.createElement("div");
    toast.textContent = "Copiado!";
    toast.className =
      "position-fixed bottom-0 end-0 m-3 bg-dark text-white px-3 py-2 rounded shadow";
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 2000);
  });
}

function mostrarJsonModal(botao) {
  const jsonString = decodeURIComponent(botao.getAttribute("data-json"));

  try {
    const json = JSON.parse(jsonString);
    const viewer = document.getElementById("jsonContent");

    // Define o conteúdo do JSON dinamicamente
    viewer.setAttribute("data", JSON.stringify(json));

    const modal = new bootstrap.Modal(document.getElementById("jsonModal"));
    modal.show();
  } catch (e) {
    console.error("Erro ao formatar JSON:", e);
    alert("Erro ao carregar JSON formatado.");
  }
}



