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

# ============================================================
# RÓTULOS E ORDENAÇÕES
# ============================================================

rotulo_carga = {
    "leve":   "Carga leve",
    "médio":  "Carga média",
    "medio":  "Carga média",
    "pesado": "Carga pesada",
}

# Cenário = linguagem + cache
# Chave: pasta no sistema de arquivos (api-py-redis, api-py-sem-redis, ...)
rotulo_cenario = {
    "api-py-redis":      "Python + Redis",
    "api-py-sem-redis":  "Python sem Redis",
    "api-ruby-redis":    "Ruby + Redis",
    "api-ruby-sem-redis":"Ruby sem Redis",
}

ordem_carga   = ["Carga leve", "Carga média", "Carga pesada"]
ordem_cenario = ["Python + Redis", "Python sem Redis", "Ruby + Redis", "Ruby sem Redis"]

# ============================================================
# LEITURA DOS CSVs
# ============================================================

linhas = []

for arquivo in sorted(pasta_resultados.rglob("*_stats.csv")):
    if arquivo.name.endswith("_stats_history.csv"):
        continue

    partes = arquivo.relative_to(pasta_resultados).parts

    # Estrutura esperada: <carga>/<cenario>/<arquivo>
    if len(partes) < 3:
        continue

    carga_raw  = partes[0]
    cenario_raw = partes[1]

    carga_label   = rotulo_carga.get(carga_raw, carga_raw)
    cenario_label = rotulo_cenario.get(cenario_raw, cenario_raw)

    # Linguagem
    linguagem = "Python" if "-py-" in cenario_raw else "Ruby"

    # Redis — corrigido: sem-redis = False, com redis = True
    tem_redis = "sem-redis" not in cenario_raw

    # Quantidade de usuários a partir do nome do arquivo
    match_usuarios = re.search(r"_(\d+)_\d+_stats\.csv$", arquivo.name)
    usuarios = int(match_usuarios.group(1)) if match_usuarios else None

    df_csv = pd.read_csv(arquivo)
    agregado = df_csv[df_csv["Name"] == "Aggregated"]
    if agregado.empty:
        agregado = df_csv.tail(1)

    linha = agregado.iloc[0]

    requisicoes = int(linha["Request Count"])
    falhas      = int(linha["Failure Count"])
    erro        = (falhas / requisicoes * 100) if requisicoes else 0

    linhas.append({
        "Carga":      carga_label,
        "CargaRaw":   carga_raw,
        "Cenario":    cenario_label,
        "CenarioRaw": cenario_raw,
        "Linguagem":  linguagem,
        "TemRedis":   tem_redis,
        "Usuarios":   usuarios,
        "Requisicoes": requisicoes,
        "Falhas":     falhas,
        "Erro":       round(erro, 2),
        "TempoMedio": float(linha["Average Response Time"]),
        "Mediana":    float(linha["Median Response Time"]),
        "P95":        float(linha["95%"]),
        "RPS":        float(linha["Requests/s"]),
    })

df = pd.DataFrame(linhas)

if df.empty:
    raise ValueError("Nenhum arquivo *_stats.csv válido foi encontrado.")

df["Carga"]   = pd.Categorical(df["Carga"],   categories=ordem_carga,   ordered=True)
df["Cenario"] = pd.Categorical(df["Cenario"], categories=ordem_cenario, ordered=True)
df = df.sort_values(["Carga", "Usuarios", "Cenario"]).reset_index(drop=True)

df.to_csv(pasta_saida / "dados_tratados_locust_trab4.csv", index=False, encoding="utf-8-sig")

print(f"Total de linhas lidas: {len(df)}")
print(df[["Carga", "Cenario", "Usuarios", "Requisicoes", "Falhas", "Erro", "TempoMedio", "P95"]].to_string())

# ============================================================
# UTILITÁRIOS DE PLOT
# ============================================================

def salvar_grafico(nome):
    plt.tight_layout()
    plt.savefig(pasta_saida / nome, dpi=300)
    plt.close()


def grafico_barra_agrupado(base, indice, colunas, valores, titulo, eixo_x, eixo_y, nome_arquivo, rotacao=0):
    tabela = base.pivot(index=indice, columns=colunas, values=valores)

    if colunas == "Carga":
        cols_existentes = [c for c in ordem_carga if c in tabela.columns]
        tabela = tabela[cols_existentes]
    if colunas == "Cenario":
        cols_existentes = [c for c in ordem_cenario if c in tabela.columns]
        tabela = tabela[cols_existentes]

    ax = tabela.plot(kind="bar", figsize=(10, 5))
    ax.set_title(titulo)
    ax.set_xlabel(eixo_x)
    ax.set_ylabel(eixo_y)
    ax.grid(True, axis="y")
    plt.xticks(rotation=rotacao)
    salvar_grafico(nome_arquivo)

# ============================================================
# GRÁFICOS GERAIS — por número de usuários (agrega cenários)
# ============================================================

def gerar_grafico_geral_por_usuarios(metrica, titulo, eixo_y, nome_arquivo):
    base = (
        df.groupby(["Cenario", "Usuarios"], observed=True, as_index=False)[metrica]
          .mean()
          .sort_values(["Cenario", "Usuarios"])
    )
    grafico_barra_agrupado(
        base=base,
        indice="Usuarios",
        colunas="Cenario",
        valores=metrica,
        titulo=titulo,
        eixo_x="Número de usuários",
        eixo_y=eixo_y,
        nome_arquivo=nome_arquivo,
    )


gerar_grafico_geral_por_usuarios(
    "TempoMedio",
    "Tempo médio por número de usuários",
    "Tempo médio (ms)",
    "01_geral_tempo_medio_por_usuarios.png",
)

gerar_grafico_geral_por_usuarios(
    "P95",
    "P95 por número de usuários",
    "P95 (ms)",
    "02_geral_p95_por_usuarios.png",
)

gerar_grafico_geral_por_usuarios(
    "Erro",
    "Taxa de falha por número de usuários",
    "Taxa de falha (%)",
    "03_geral_taxa_falha_por_usuarios.png",
)

# ============================================================
# GRÁFICOS GERAIS — por cenário (agrega cargas)
# ============================================================

def gerar_grafico_geral_por_cenario(metrica, titulo, eixo_y, nome_arquivo):
    base = (
        df.groupby(["Carga", "Cenario"], observed=True, as_index=False)[metrica]
          .mean()
          .sort_values(["Carga", "Cenario"])
    )
    grafico_barra_agrupado(
        base=base,
        indice="Cenario",
        colunas="Carga",
        valores=metrica,
        titulo=titulo,
        eixo_x="Cenário",
        eixo_y=eixo_y,
        nome_arquivo=nome_arquivo,
        rotacao=15,
    )


gerar_grafico_geral_por_cenario(
    "TempoMedio",
    "Tempo médio por cenário",
    "Tempo médio (ms)",
    "04_geral_tempo_medio_por_cenario.png",
)

gerar_grafico_geral_por_cenario(
    "P95",
    "P95 por cenário",
    "P95 (ms)",
    "05_geral_p95_por_cenario.png",
)

gerar_grafico_geral_por_cenario(
    "Erro",
    "Taxa de falha por cenário",
    "Taxa de falha (%)",
    "06_geral_taxa_falha_por_cenario.png",
)

# ============================================================
# GRÁFICOS POR LINGUAGEM — Python vs Ruby, com e sem Redis
# ============================================================

def grafico_por_linguagem(linguagem, metrica, titulo, eixo_y, nome_arquivo):
    base = df[df["Linguagem"] == linguagem].copy()
    if base.empty:
        print(f"Aviso: sem dados para linguagem {linguagem}.")
        return

    base = (
        base.groupby(["Usuarios", "Cenario"], observed=True, as_index=False)[metrica]
            .mean()
            .sort_values(["Usuarios", "Cenario"])
    )

    tabela = base.pivot(index="Usuarios", columns="Cenario", values=metrica)
    cols = [c for c in ordem_cenario if c in tabela.columns]
    tabela = tabela[cols]

    ax = tabela.plot(kind="bar", figsize=(10, 5))
    ax.set_title(titulo)
    ax.set_xlabel("Número de usuários")
    ax.set_ylabel(eixo_y)
    ax.grid(True, axis="y")
    plt.xticks(rotation=0)
    salvar_grafico(nome_arquivo)


def gerar_graficos_linguagem(linguagem, slug):
    grafico_por_linguagem(
        linguagem, "TempoMedio",
        f"Tempo médio — {linguagem} (com e sem Redis)",
        "Tempo médio (ms)",
        f"{slug}_tempo_medio.png",
    )
    grafico_por_linguagem(
        linguagem, "P95",
        f"P95 — {linguagem} (com e sem Redis)",
        "P95 (ms)",
        f"{slug}_p95.png",
    )
    grafico_por_linguagem(
        linguagem, "Erro",
        f"Taxa de falha — {linguagem} (com e sem Redis)",
        "Taxa de falha (%)",
        f"{slug}_taxa_falha.png",
    )


gerar_graficos_linguagem("Python", "07_python")
gerar_graficos_linguagem("Ruby",   "08_ruby")

# ============================================================
# GRÁFICOS COM vs SEM REDIS — Python e Ruby juntos
# ============================================================

def grafico_redis_vs_sem(tem_redis, metrica, titulo, eixo_y, nome_arquivo):
    base = df[df["TemRedis"] == tem_redis].copy()
    if base.empty:
        return

    base = (
        base.groupby(["Usuarios", "Cenario"], observed=True, as_index=False)[metrica]
            .mean()
            .sort_values(["Usuarios", "Cenario"])
    )

    tabela = base.pivot(index="Usuarios", columns="Cenario", values=metrica)
    cols = [c for c in ordem_cenario if c in tabela.columns]
    tabela = tabela[cols]

    ax = tabela.plot(kind="bar", figsize=(10, 5))
    ax.set_title(titulo)
    ax.set_xlabel("Número de usuários")
    ax.set_ylabel(eixo_y)
    ax.grid(True, axis="y")
    plt.xticks(rotation=0)
    salvar_grafico(nome_arquivo)


def gerar_graficos_redis(tem_redis, slug, label):
    grafico_redis_vs_sem(tem_redis, "TempoMedio", f"Tempo médio — {label}", "Tempo médio (ms)", f"{slug}_tempo_medio.png")
    grafico_redis_vs_sem(tem_redis, "P95",        f"P95 — {label}",         "P95 (ms)",          f"{slug}_p95.png")
    grafico_redis_vs_sem(tem_redis, "Erro",       f"Taxa de falha — {label}", "Taxa de falha (%)", f"{slug}_taxa_falha.png")


gerar_graficos_redis(True,  "09_com_redis",  "com Redis")
gerar_graficos_redis(False, "10_sem_redis",  "sem Redis")


print("\nGráficos gerados com sucesso na pasta 'graficos'.")
print("Gráficos gerais por usuários:  3  (01–03)")
print("Gráficos gerais por cenário:   3  (04–06)")
print("Gráficos Python (com/sem):     3  (07)")
print("Gráficos Ruby (com/sem):       3  (08)")
print("Gráficos com Redis:            3  (09)")
print("Gráficos sem Redis:            3  (10)")
print("Total:                        18 gráficos")