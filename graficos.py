import os
import pandas as pd
import matplotlib.pyplot as plt


dados = [
    ["Carga leve", "Imagem 1MB", 1, 150, 2933, 0, 0.00, 109, 83, 270, 24.50],
    ["Carga leve", "Imagem 300KB", 1, 150, 2803, 0, 0.00, 106, 83, 260, 23.42],
    ["Carga leve", "Texto 400KB", 1, 150, 2864, 0, 0.00, 112, 90, 260, 23.93],

    ["Carga média", "Imagem 1MB", 1, 300, 5376, 0, 0.00, 280, 210, 680, 44.84],
    ["Carga média", "Imagem 300KB", 1, 300, 5195, 0, 0.00, 273, 190, 670, 43.33],
    ["Carga média", "Texto 400KB", 1, 300, 5200, 0, 0.00, 289, 220, 700, 43.38],

    ["Carga pesada", "Imagem 1MB", 1, 1500, 14820, 12411, 83.74, 1605, 210, 9700, 123.25],
    ["Carga pesada", "Imagem 300KB", 1, 1500, 14824, 12397, 83.63, 1583, 240, 9600, 123.28],
    ["Carga pesada", "Texto 400KB", 1, 1500, 14823, 12399, 83.65, 1631, 240, 9700, 123.27],

    ["Carga leve", "Imagem 1MB", 2, 150, 2793, 0, 0.00, 131, 110, 320, 23.31],
    ["Carga leve", "Imagem 300KB", 2, 150, 2896, 0, 0.00, 130, 100, 310, 24.17],
    ["Carga leve", "Texto 400KB", 2, 150, 2771, 0, 0.00, 141, 110, 330, 23.13],

    ["Carga média", "Imagem 1MB", 2, 300, 4786, 0, 0.00, 473, 400, 1000, 40.06],
    ["Carga média", "Imagem 300KB", 2, 300, 4854, 0, 0.00, 469, 400, 1000, 40.62],
    ["Carga média", "Texto 400KB", 2, 300, 4841, 0, 0.00, 499, 430, 1000, 40.52],

    ["Carga pesada", "Imagem 1MB", 2, 1500, 9100, 4721, 51.88, 3609, 1600, 18000, 74.14],
    ["Carga pesada", "Imagem 300KB", 2, 1500, 9203, 4708, 51.16, 3678, 1600, 18000, 74.98],
    ["Carga pesada", "Texto 400KB", 2, 1500, 9261, 4776, 51.57, 3801, 1700, 19000, 75.45],

    ["Carga leve", "Imagem 1MB", 3, 150, 2722, 0, 0.00, 128, 97, 320, 22.73],
    ["Carga leve", "Imagem 300KB", 3, 150, 2872, 0, 0.00, 133, 99, 310, 23.99],
    ["Carga leve", "Texto 400KB", 3, 150, 2807, 0, 0.00, 135, 110, 320, 23.44],

    ["Carga média", "Imagem 1MB", 3, 300, 5409, 0, 0.00, 240, 160, 600, 45.28],
    ["Carga média", "Imagem 300KB", 3, 300, 5304, 0, 0.00, 234, 160, 570, 44.40],
    ["Carga média", "Texto 400KB", 3, 300, 5312, 0, 0.00, 248, 170, 600, 44.47],

    ["Carga pesada", "Imagem 1MB", 3, 1500, 11607, 6241, 53.77, 2489, 1100, 11000, 95.62],
    ["Carga pesada", "Imagem 300KB", 3, 1500, 11614, 6133, 52.81, 2487, 1100, 11000, 95.68],
    ["Carga pesada", "Texto 400KB", 3, 1500, 11877, 6309, 53.12, 2590, 1200, 12000, 97.84],
]

colunas = [
    "Teste",
    "Conteudo",
    "Instancias",
    "Usuarios",
    "Requisicoes",
    "Falhas",
    "Erro",
    "TempoMedio",
    "Mediana",
    "P95",
    "RPS",
]

df = pd.DataFrame(dados, columns=colunas)

ordem_testes = ["Carga leve", "Carga média", "Carga pesada"]
df["Teste"] = pd.Categorical(df["Teste"], categories=ordem_testes, ordered=True)

pasta_saida = "graficos"
os.makedirs(pasta_saida, exist_ok=True)


def salvar_grafico(nome):
    caminho = os.path.join(pasta_saida, nome)
    plt.tight_layout()
    plt.savefig(caminho, dpi=300)
    plt.close()


def gerar_grafico_por_usuarios(metrica, titulo, eixo_y, nome_arquivo):
    base = (
        df.groupby(["Instancias", "Usuarios"], as_index=False)[metrica]
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
        df.groupby(["Teste", "Instancias"], as_index=False)[metrica]
        .mean()
        .sort_values(["Teste", "Instancias"])
    )

    plt.figure(figsize=(9, 5))

    for teste in ordem_testes:
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
        df.groupby(["Teste", "Conteudo"], as_index=False)["TempoMedio"]
        .mean()
        .sort_values(["Teste", "Conteudo"])
    )

    tabela = base.pivot(index="Conteudo", columns="Teste", values="TempoMedio")
    tabela = tabela[ordem_testes]

    ax = tabela.plot(kind="bar", figsize=(10, 5))
    ax.set_title("Tempo médio por tipo de conteúdo")
    ax.set_xlabel("Tipo de conteúdo")
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

df.to_csv(os.path.join(pasta_saida, "dados_testes_locust.csv"), index=False, encoding="utf-8-sig")

print("Gráficos gerados com sucesso na pasta 'graficos'.")