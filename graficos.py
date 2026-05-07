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

    raise FileNotFoundError("Não encontrei a pasta de resultados.")


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

ordem_testes = ["Carga leve", "Carga média", "Carga pesada"]
ordem_conteudos = ["Imagem 1MB", "Imagem 300KB", "Texto 400KB", "Todos"]

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
        "ArquivoOrigem": str(arquivo),
    })

df = pd.DataFrame(linhas)

if df.empty:
    raise ValueError("Nenhum arquivo *_stats.csv válido foi encontrado.")

df["Teste"] = pd.Categorical(df["Teste"], categories=ordem_testes, ordered=True)
df["Conteudo"] = pd.Categorical(df["Conteudo"], categories=ordem_conteudos, ordered=True)
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


def grafico_barra_agrupado(base, indice, colunas, valores, titulo, eixo_x, eixo_y, nome_arquivo, rotacao=0):
    tabela = base.pivot(index=indice, columns=colunas, values=valores)

    if colunas == "Teste":
        colunas_existentes = [c for c in ordem_testes if c in tabela.columns]
        tabela = tabela[colunas_existentes]

    if indice == "Conteudo":
        tabela = tabela.reindex([c for c in ordem_conteudos if c in tabela.index])

    ax = tabela.plot(kind="bar", figsize=(10, 5))
    ax.set_title(titulo)
    ax.set_xlabel(eixo_x)
    ax.set_ylabel(eixo_y)
    ax.grid(True, axis="y")
    plt.xticks(rotation=rotacao)
    salvar_grafico(nome_arquivo)


# ============================================================
# GRÁFICOS GERAIS ANTIGOS
# Estes mantêm a visão geral agregando todos os cenários:
# Imagem 1MB + Imagem 300KB + Texto 400KB + Todos
# ============================================================

def gerar_grafico_geral_por_usuarios(metrica, titulo, eixo_y, nome_arquivo):
    base = (
        df.groupby(["Instancias", "Usuarios"], observed=True, as_index=False)[metrica]
          .mean()
          .sort_values(["Instancias", "Usuarios"])
    )

    grafico_barra_agrupado(
        base=base,
        indice="Usuarios",
        colunas="Instancias",
        valores=metrica,
        titulo=titulo,
        eixo_x="Número de usuários",
        eixo_y=eixo_y,
        nome_arquivo=nome_arquivo
    )


def gerar_grafico_geral_por_instancias(metrica, titulo, eixo_y, nome_arquivo):
    base = (
        df.groupby(["Teste", "Instancias"], observed=True, as_index=False)[metrica]
          .mean()
          .sort_values(["Teste", "Instancias"])
    )

    grafico_barra_agrupado(
        base=base,
        indice="Instancias",
        colunas="Teste",
        valores=metrica,
        titulo=titulo,
        eixo_x="Quantidade de instâncias WordPress",
        eixo_y=eixo_y,
        nome_arquivo=nome_arquivo
    )


gerar_grafico_geral_por_usuarios(
    "TempoMedio",
    "Tempo médio geral por número de usuários",
    "Tempo médio (ms)",
    "01_geral_tempo_medio_por_usuarios.png"
)

gerar_grafico_geral_por_usuarios(
    "P95",
    "P95 geral por número de usuários",
    "P95 (ms)",
    "02_geral_p95_por_usuarios.png"
)

gerar_grafico_geral_por_usuarios(
    "Erro",
    "Taxa de falha geral por número de usuários",
    "Taxa de falha (%)",
    "03_geral_taxa_falha_por_usuarios.png"
)

gerar_grafico_geral_por_usuarios(
    "RPS",
    "Requisições por segundo geral por número de usuários",
    "RPS",
    "04_geral_rps_por_usuarios.png"
)

gerar_grafico_geral_por_instancias(
    "TempoMedio",
    "Tempo médio geral por quantidade de instâncias",
    "Tempo médio (ms)",
    "05_geral_tempo_medio_por_instancias.png"
)

gerar_grafico_geral_por_instancias(
    "P95",
    "P95 geral por quantidade de instâncias",
    "P95 (ms)",
    "06_geral_p95_por_instancias.png"
)

gerar_grafico_geral_por_instancias(
    "Erro",
    "Taxa de falha geral por quantidade de instâncias",
    "Taxa de falha (%)",
    "07_geral_taxa_falha_por_instancias.png"
)

gerar_grafico_geral_por_instancias(
    "RPS",
    "Requisições por segundo geral por quantidade de instâncias",
    "RPS",
    "08_geral_rps_por_instancias.png"
)


# ============================================================
# NOVOS GRÁFICOS POR TIPO DE CONTEÚDO
# 4 tipos de conteúdo x 3 métricas = 12 gráficos
# Cada gráfico usa somente um tipo de conteúdo por vez.
# ============================================================

def grafico_barra_por_conteudo(conteudo, metrica, titulo, eixo_y, nome_arquivo):
    base = df[df["Conteudo"] == conteudo].copy()

    if base.empty:
        print(f"Aviso: não foram encontrados dados para {conteudo}.")
        return

    base = (
        base.groupby(["Usuarios", "Instancias"], observed=True, as_index=False)[metrica]
            .mean()
            .sort_values(["Usuarios", "Instancias"])
    )

    tabela = base.pivot(index="Usuarios", columns="Instancias", values=metrica)

    ax = tabela.plot(kind="bar", figsize=(10, 5))
    ax.set_title(titulo)
    ax.set_xlabel("Número de usuários")
    ax.set_ylabel(eixo_y)
    ax.grid(True, axis="y")
    plt.xticks(rotation=0)

    salvar_grafico(nome_arquivo)


def gerar_graficos_para_conteudo(conteudo, slug):
    grafico_barra_por_conteudo(
        conteudo=conteudo,
        metrica="TempoMedio",
        titulo=f"Tempo médio - {conteudo}",
        eixo_y="Tempo médio (ms)",
        nome_arquivo=f"{slug}_tempo_medio.png"
    )

    grafico_barra_por_conteudo(
        conteudo=conteudo,
        metrica="P95",
        titulo=f"P95 - {conteudo}",
        eixo_y="P95 (ms)",
        nome_arquivo=f"{slug}_p95.png"
    )

    grafico_barra_por_conteudo(
        conteudo=conteudo,
        metrica="Erro",
        titulo=f"Taxa de falha - {conteudo}",
        eixo_y="Taxa de falha (%)",
        nome_arquivo=f"{slug}_taxa_falha.png"
    )


gerar_graficos_para_conteudo("Imagem 1MB", "09_imagem_1mb")
gerar_graficos_para_conteudo("Imagem 300KB", "10_imagem_300kb")
gerar_graficos_para_conteudo("Texto 400KB", "11_texto_400kb")
gerar_graficos_para_conteudo("Todos", "12_todos")


print("Gráficos gerados com sucesso na pasta 'graficos'.")
print(f"Total de cenários lidos: {len(df)}")
print("Gráficos gerais gerados: 8")
print("Gráficos por conteúdo gerados: 12")
print("Total de gráficos gerados: 20")
