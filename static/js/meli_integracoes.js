function testarConexao(id) {
  fetch(`/dashboard/meli_integracoes/me/${id}`)
    .then(async (response) => {
      try {
            return await response.json();
        } catch {
            return { error: "Resposta inválida da API", raw: response };
        }
    })
    .then((data) => {
        const viewer = document.getElementById("jsonContent");
        viewer.setAttribute("data", JSON.stringify(data));
        const modal = new bootstrap.Modal(document.getElementById("jsonModal"));
        modal.show();
    })
    .catch((error) => {
      pre.textContent = `Erro: ${error}`;
      modal.show();
        console.error(`Erro: ${error}`);
        alert("Erro ao carregar JSON formatado.");
    });
}

function safeValue(val, defaultVal = "N/D") {
  return val !== undefined && val !== null && val !== "" ? val : defaultVal;
}

function badgeColor(levelId) {
  switch (levelId) {
    case "5_green":
    case "4_light_green":
      return "bg-success";
    case "3_yellow":
      return "bg-warning";
    case "2_orange":
      return "bg-orange"; // defina no CSS se ainda não existir
    case "1_red":
      return "bg-danger";
    default:
      return "bg-secondary";
  }
}

function analisarReputacao(id) {
  const modal = new bootstrap.Modal(document.getElementById("modalReputacao"));
  const raw = document.getElementById("conteudoReputacaoRaw");
  raw.classList.add("d-none");
  raw.textContent = "";

  fetch(`/dashboard/meli_integracoes/reputacao/${id}`)
    .then((r) => r.json())
    .then((d) => {
      if (d.status !== "success") {
        raw.classList.remove("d-none");
        raw.textContent = `Erro: ${d.message}`;
        modal.show();
        return;
      }

      const i = d.data;

      document.getElementById("reputacaoNickname").textContent = safeValue(
        i.nickname
      );
      document.getElementById("reputacaoPowerSeller").textContent = safeValue(
        i.status_power_seller
      );

      const nivel = document.getElementById("reputacaoNivel");
      nivel.textContent = safeValue(i.nivel_reputacao);
      nivel.className = "badge " + badgeColor(i.nivel_reputacao);

      document.getElementById("transCompletas").textContent = safeValue(
        i.pontuacao.completed
      );
      document.getElementById("transCanceladas").textContent = safeValue(
        i.pontuacao.canceled
      );
      document.getElementById("transTotal").textContent = safeValue(
        i.pontuacao.total
      );

      document.getElementById("metricaClaims").textContent =
        safeValue(i.avaliacoes.claims) + "%";
      document.getElementById("metricaDelayed").textContent =
        safeValue(i.avaliacoes.delayed) + "%";
      document.getElementById("metricaCanceled").textContent =
        safeValue(i.avaliacoes.cancellations) + "%";

      document.getElementById("taxaPositiva").textContent =
        safeValue(i.pontuacao.ratings.positive) + "%";
      document.getElementById("taxaNegativa").textContent =
        safeValue(i.pontuacao.ratings.negative) + "%";
      document.getElementById("taxaNeutra").textContent =
        safeValue(i.pontuacao.ratings.neutral) + "%";

      document.getElementById("reputacaoStatus").textContent = safeValue(
        i.status
      );
      document.getElementById("reputacaoCadastro").textContent =
        i.cadastro !== "N/D"
          ? new Date(i.cadastro).toLocaleDateString()
          : "N/D";
      document.getElementById("reputacaoTipoVendedor").textContent = safeValue(
        i.tipo_vendedor
      );

      document.getElementById("reputacaoTaxaResposta").textContent =
        i.atendimento.taxa_resposta != null
          ? (i.atendimento.taxa_resposta * 100).toFixed(1) + "%"
          : "N/D";

      document.getElementById("reputacaoTempoMedio").textContent =
        i.atendimento.tempo_medio != null
          ? Math.round(i.atendimento.tempo_medio / 1000) + "s"
          : "N/D";

      modal.show();
    })
    .catch((e) => {
      raw.classList.remove("d-none");
      raw.textContent = `Erro: ${e}`;
      modal.show();
    });
}
