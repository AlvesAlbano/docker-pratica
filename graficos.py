from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


OUTPUT_DIR = Path("./graficos")
OUTPUT_DIR.mkdir(exist_ok=True)


def load_data():
    df_http = pd.read_csv("csv_junto.csv")
    df_grpc = pd.read_csv("grpc_stats.csv")

    # padronizar nomes
    df_http["tipo_api"] = df_http["tipo_api"].str.lower()
    df_grpc["tipo_api"] = df_grpc["tipo_api"].str.lower()

    # manter apenas colunas comuns
    common_cols = list(
        set(df_http.columns).intersection(df_grpc.columns)
    )

    df = pd.concat(
        [
            df_http[common_cols],
            df_grpc[common_cols]
        ],
        ignore_index=True
    )

    return df


def aggregate(df):
    """
    Média das métricas por tecnologia e linguagem.
    """

    return (
        df.groupby(
            ["tipo_api", "linguagem"],
            as_index=False
        )
        .agg(
            {
                "Average Response Time": "mean",
                "95%": "mean",
                "Requests/s": "mean",
            }
        )
    )


def plot_avg_latency(df):
    pivot = df.pivot(
        index="tipo_api",
        columns="linguagem",
        values="Average Response Time"
    )

    plt.figure(figsize=(10, 6))

    pivot.plot(
        kind="bar",
        ax=plt.gca()
    )

    plt.title(
        "Latência Média por Linguagem"
    )
    plt.xlabel("Linguagem")
    plt.ylabel("Average Response Time (ms)")
    plt.xticks(rotation=0)

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "01_latencia_media.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


def plot_p95(df):
    pivot = df.pivot(
        index="tipo_api",
        columns="linguagem",
        values="95%"
    )

    plt.figure(figsize=(10, 6))

    pivot.plot(
        kind="bar",
        ax=plt.gca()
    )

    plt.title(
        "P95 por Linguagem"
    )
    plt.xlabel("Linguagem")
    plt.ylabel("P95 (ms)")
    plt.xticks(rotation=0)

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "02_p95.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


def plot_rps(df):
    pivot = df.pivot(
        index="tipo_api",
        columns="linguagem",
        values="Requests/s"
    )

    plt.figure(figsize=(10, 6))

    pivot.plot(
        kind="bar",
        ax=plt.gca()
    )

    plt.title(
        "Requisições/s por Linguagem"
    )
    plt.xlabel("Linguagem")
    plt.ylabel("Requests/s")
    plt.xticks(rotation=0)

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "03_requests_per_second.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


def plot_metric_by_language(
    df,
    language,
    metric,
    title,
    filename,
    ylabel,
):
    lang_df = df[
        df["linguagem"].str.lower() == language.lower()
    ]

    values = (
        lang_df
        .groupby("tipo_api")[metric]
        .mean()
        .sort_index()
    )

    plt.figure(figsize=(10, 6))

    values.plot(kind="bar")

    plt.title(title)
    plt.xlabel("Tecnologia")
    plt.ylabel(ylabel)

    plt.xticks(rotation=0)

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / filename,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

def plot_error_rate_comparison(df):

    agg = (
        df.groupby(
            ["tipo_api", "linguagem"]
        )["Error Rate (%)"]
        .mean()
        .reset_index()
    )

    pivot = agg.pivot(
        index="tipo_api",
        columns="linguagem",
        values="Error Rate (%)"
    )

    plt.figure(figsize=(10, 6))

    pivot.plot(
        kind="bar",
        ax=plt.gca()
    )

    plt.title(
        "Taxa de Erro por Tecnologia"
    )

    plt.xlabel("Tecnologia")
    plt.ylabel("Taxa de Erro (%)")

    plt.xticks(rotation=0)

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR /
        "04_taxa_erro_comparativo.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

def plot_error_rate_comparison_por_carga(
        df,
        linguagem:str=None,
        carga:str=None
):


    df = df[
        df["linguagem"].str.lower()
        == linguagem.lower()
    ]

    agg = (
        df.groupby(["tipo_api", "linguagem"])["Error Rate (%)"]
        .mean()
        .reset_index()
    )

    pivot = agg.pivot(
        index="tipo_api",
        columns="linguagem",
        values="Error Rate (%)"
    )

    plt.figure(figsize=(10, 6))

    pivot.plot(
        kind="bar",
        ax=plt.gca()
    )

    plt.title(
        f"Taxa de Erro por Tecnologia - {carga.capitalize()}"
    )

    plt.xlabel("Tecnologia")
    plt.ylabel("Taxa de Erro (%)")

    plt.xticks(rotation=0)

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR /
        f"taxa_erro_{linguagem}_{carga}.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

def plot_error_rate_by_language(
    df,
    language
):

    lang_df = df[
        df["linguagem"].str.lower()
        == language.lower()
    ]

    values = (
        lang_df
        .groupby("tipo_api")
        ["Error Rate (%)"]
        .mean()
    )

    plt.figure(figsize=(10, 6))

    values.plot(kind="bar")

    plt.title(
        f"Taxa de Erro - {language.capitalize()}"
    )

    plt.xlabel("Tecnologia")
    plt.ylabel("Taxa de Erro (%)")

    plt.xticks(rotation=0)

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR /
        f"taxa_erro_{language}.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


def plot_error_rate_by_language_por_carga(
    df,
    language:str,
    carga:str
):

    df = df[
        df["linguagem"].str.lower()
        == language.lower()
    ]

    values = (
        df.groupby("tipo_api")["Error Rate (%)"]
        .mean()
    )

    plt.figure(figsize=(10, 6))

    values.plot(kind="bar")

    plt.title(
        f"Taxa de Erro - {language.capitalize()} ({carga})"
    )

    plt.xlabel("Tecnologia")
    plt.ylabel("Taxa de Erro (%)")

    plt.xticks(rotation=0)

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR /
        f"taxa_erro_{language}_{carga}.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

def generate_all_graphs(df):
    df = df.copy()

    df["Error Rate (%)"] = (
        df["Failure Count"] / df["Request Count"]
    ) * 100

    df_agg = aggregate(df)

    plot_avg_latency(df_agg)
    plot_p95(df_agg)
    plot_rps(df_agg)

    plot_metric_by_language(
        df_agg,
        "java",
        "Average Response Time",
        "Latência Média - Java",
        "latencia_media_java.png",
        "Latência Média (ms)",
    )

    plot_metric_by_language(
        df_agg,
        "java",
        "95%",
        "P95 - Java",
        "p95_java.png",
        "P95 (ms)",
    )

    plot_metric_by_language(
        df_agg,
        "java",
        "Requests/s",
        "Requisições por Segundo - Java",
        "rps_java.png",
        "Requisições/s",
    )

    plot_metric_by_language(
        df_agg,
        "kotlin",
        "Average Response Time",
        "Latência Média - Kotlin",
        "latencia_media_kotlin.png",
        "Latência Média (ms)",
    )

    plot_metric_by_language(
        df_agg,
        "kotlin",
        "95%",
        "P95 - Kotlin",
        "p95_kotlin.png",
        "P95 (ms)",
    )

    plot_metric_by_language(
        df_agg,
        "kotlin",
        "Requests/s",
        "Requisições por Segundo - Kotlin",
        "rps_kotlin.png",
        "Requisições/s",
    )

    plot_error_rate_comparison(df)
    plot_error_rate_by_language(df, "java")
    plot_error_rate_by_language(df, "kotlin")


def generate_all_graphs_por_carga(df,linguagem:str,carga_tipo:str):
    df = df.copy()

    df["Error Rate (%)"] = (
        df["Failure Count"] / df["Request Count"]
    ) * 100

    df_agg = aggregate(df)

    plot_avg_latency(df_agg)
    plot_p95(df_agg)
    plot_rps(df_agg)

    plot_metric_by_language(
        df_agg,
        linguagem,
        "Average Response Time",
        f"Latência Média - {linguagem.capitalize()} - {carga_tipo.capitalize()}",
        f"latencia_media_{linguagem}_{carga_tipo}.png",
        "Latência Média (ms)",
    )

    plot_metric_by_language(
        df_agg,
        linguagem,
        "95%",
        f"P95 - {linguagem.capitalize()} - {carga_tipo.capitalize()}",
        f"p95_{linguagem}__{carga_tipo}.png",
        "P95 (ms)",
    )

    plot_metric_by_language(
        df_agg,
        linguagem,
        "Requests/s",
        f"Requisições por Segundo - {linguagem.capitalize()} - {carga_tipo.capitalize()}",
        f"rps_{linguagem}_{carga_tipo}.png",
        "Requisições/s",
    )

    plot_error_rate_comparison_por_carga(df,linguagem,carga_tipo)

    plot_error_rate_by_language_por_carga(df, linguagem,carga_tipo)

def main():
    global OUTPUT_DIR

    df = load_data()

    # ==================================
    # Todos os dados
    # ==================================

    OUTPUT_DIR = Path("./graficos/todos")
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    generate_all_graphs(df)

    # ==================================
    # Por carga
    # ==================================


    for linguagem in ["java","kotlin"]:
        for carga in ["leve","medio","pesado"]:

            df_filtrado = df[
                (df["linguagem"].str.lower() == linguagem.lower())
                &
                (df["carga"].str.lower() == carga.lower())
            ]

            OUTPUT_DIR = Path(
                f"./graficos/{linguagem}/{carga}"
            )

            OUTPUT_DIR.mkdir(
                parents=True,
                exist_ok=True
            )

            generate_all_graphs_por_carga(df_filtrado,linguagem,carga)

            print(
                f"Gráficos gerados para carga: {carga}"
            )

        print(
            "\nTodos os gráficos foram gerados."
        )

if __name__ == "__main__":
    main()