import os
import re
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


def encontrar_pasta_resultados():
    opcoes = [
        Path("locust") / "resultados",
        Path("resultados"),
    ]

    for pasta in opcoes:
        if pasta.exists():
            return pasta

    raise FileNotFoundError(
        "Não encontrei a pasta de resultados. "
    )


pasta_resultados = encontrar_pasta_resultados()
pasta_saida = Path("graficos")
pasta_saida.mkdir(exist_ok=True)

rotulo_carga = {
    "leve": "Carga leve",
    "medio": "Carga média",
    "pesado": "Carga pesada",
}

rotulo_cenario = {
    "post_imagem_1mb": "Imagem 1MB",
    "post_imagem_300kb": "Imagem 300KB",
    "post_texto_400kb": "Texto 400KB",
    "todos": "Todos",
}

linhas = []

for arquivo in sorted(pasta_resultados.rglob("*_stats.csv")):
    if arquivo.name.endswith("_stats_history.csv"):
        continue

    partes = arquivo.relative_to(pasta_resultados).parts

    if len(partes) < 4:
        continue

    carga = partes[0]
    instancia_txt = partes[1]
    cenario = partes[2]

    try:
        instancia = int(instancia_txt.replace("instancia_", ""))
    except ValueError:
        continue

    match_usuarios = re.search(r"_(\d+)_usuarios_stats\.csv$", arquivo.name)
    usuarios = int(match_usuarios.group(1)) if match_usuarios else None

    df_csv = pd.read_csv(arquivo)
    agregado = df_csv[df_csv["Name"] == "Aggregated"]

    if agregado.empty:
        agregado = df_csv.tail(1)

    linha = agregado.iloc[0]

    requisicoes = int(linha["Request Count"])
    falhas = int(linha["Failure Count"])
    erro = (falhas / requisicoes * 100) if requisicoes else 0

    linhas.append({
        "Teste": rotulo_carga.get(carga, carga),
        "Carga": carga,
        "Conteudo": rotulo_cenario.get(cenario, cenario),
        "Cenario": cenario,
        "Instancias": instancia,
        "Usuarios": usuarios,
        "Requisicoes": requisicoes,
        "Falhas": falhas,
        "Erro": erro,
        "TempoMedio": float(linha["Average Response Time"]),
        "Mediana": float(linha["Median Response Time"]),
        "P95": float(linha["95%"]),
        "RPS": float(linha["Requests/s"]),
        # "ArquivoOrigem": str(arquivo),
    })

df = pd.DataFrame(linhas)

if df.empty:
    raise ValueError("Nenhum arquivo *_stats.csv válido foi encontrado.")

df["Teste"] = pd.Categorical(
    df["Teste"],
    categories=["Carga leve", "Carga média", "Carga pesada"],
    ordered=True
)

df["Conteudo"] = pd.Categorical(
    df["Conteudo"],
    categories=["Imagem 1MB", "Imagem 300KB", "Texto 400KB", "Todos"],
    ordered=True
)

df = df.sort_values(["Teste", "Instancias", "Conteudo"]).reset_index(drop=True)

df.to_csv(pasta_saida / "dados_tratados_locust_36_testes.csv", index=False, encoding="utf-8-sig")

df_geral = (
    df.groupby(["Teste", "Usuarios", "Instancias"], observed=True, as_index=False)
      .agg({
          "Requisicoes": "sum",
          "Falhas": "sum",
          "TempoMedio": "mean",
          "Mediana": "mean",
          "P95": "mean",
          "RPS": "mean",
      })
)

df_geral["Erro"] = (df_geral["Falhas"] / df_geral["Requisicoes"] * 100).fillna(0)
df_geral = df_geral[[
    "Teste", "Usuarios", "Instancias", "Requisicoes", "Falhas",
    "Erro", "TempoMedio", "Mediana", "P95", "RPS"
]]

df_geral.to_csv(pasta_saida / "resumo_geral_por_carga_instancia.csv", index=False, encoding="utf-8-sig")


def salvar_grafico(nome):
    plt.tight_layout()
    plt.savefig(pasta_saida / nome, dpi=300)
    plt.close()


def gerar_grafico_por_usuarios(metrica, titulo, eixo_y, nome_arquivo):
    base = (
        df.groupby(["Instancias", "Usuarios"], observed=True, as_index=False)[metrica]
          .mean()
          .sort_values(["Instancias", "Usuarios"])
    )

    plt.figure(figsize=(9, 5))

    for instancia in sorted(base["Instancias"].unique()):
        dados_instancia = base[base["Instancias"] == instancia]
        plt.plot(
            dados_instancia["Usuarios"],
            dados_instancia[metrica],
            marker="o",
            label=f"{instancia} instância(s)"
        )

    plt.title(titulo)
    plt.xlabel("Número de usuários")
    plt.ylabel(eixo_y)
    plt.legend()
    plt.grid(True)
    salvar_grafico(nome_arquivo)


def gerar_grafico_por_instancias(metrica, titulo, eixo_y, nome_arquivo):
    base = (
        df.groupby(["Teste", "Instancias"], observed=True, as_index=False)[metrica]
          .mean()
          .sort_values(["Teste", "Instancias"])
    )

    plt.figure(figsize=(9, 5))

    for teste in ["Carga leve", "Carga média", "Carga pesada"]:
        dados_teste = base[base["Teste"] == teste]
        plt.plot(
            dados_teste["Instancias"],
            dados_teste[metrica],
            marker="o",
            label=teste
        )

    plt.title(titulo)
    plt.xlabel("Quantidade de instâncias WordPress")
    plt.ylabel(eixo_y)
    plt.xticks([1, 2, 3])
    plt.legend()
    plt.grid(True)
    salvar_grafico(nome_arquivo)


def gerar_grafico_conteudo():
    base = (
        df.groupby(["Teste", "Conteudo"], observed=True, as_index=False)["TempoMedio"]
          .mean()
          .sort_values(["Teste", "Conteudo"])
    )

    tabela = base.pivot(index="Conteudo", columns="Teste", values="TempoMedio")
    tabela = tabela[["Carga leve", "Carga média", "Carga pesada"]]

    ax = tabela.plot(kind="bar", figsize=(10, 5))
    ax.set_title("Tempo médio por cenário de conteúdo")
    ax.set_xlabel("Cenário de conteúdo")
    ax.set_ylabel("Tempo médio (ms)")
    ax.grid(True, axis="y")

    plt.xticks(rotation=0)
    salvar_grafico("08_tempo_medio_por_conteudo.png")


gerar_grafico_por_usuarios(
    "TempoMedio",
    "Tempo médio por número de usuários",
    "Tempo médio (ms)",
    "01_tempo_medio_por_usuarios.png"
)

gerar_grafico_por_usuarios(
    "P95",
    "P95 por número de usuários",
    "P95 (ms)",
    "02_p95_por_usuarios.png"
)

gerar_grafico_por_usuarios(
    "Erro",
    "Taxa de erro por número de usuários",
    "Erro (%)",
    "03_erro_por_usuarios.png"
)

gerar_grafico_por_usuarios(
    "RPS",
    "Requisições por segundo por número de usuários",
    "RPS",
    "04_rps_por_usuarios.png"
)

gerar_grafico_por_instancias(
    "TempoMedio",
    "Tempo médio por quantidade de instâncias",
    "Tempo médio (ms)",
    "05_tempo_medio_por_instancias.png"
)

gerar_grafico_por_instancias(
    "P95",
    "P95 por quantidade de instâncias",
    "P95 (ms)",
    "06_p95_por_instancias.png"
)

gerar_grafico_por_instancias(
    "Erro",
    "Taxa de erro por quantidade de instâncias",
    "Erro (%)",
    "07_erro_por_instancias.png"
)

gerar_grafico_conteudo()

print("Gráficos gerados com sucesso na pasta 'graficos'.")
print(f"Total de cenários lidos: {len(df)}")
