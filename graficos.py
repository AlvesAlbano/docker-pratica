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
        f"{language}_taxa_erro.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


def main():
    df = load_data()
    
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
        "java_latencia_media.png",
        "Latência Média (ms)",
    )

    plot_metric_by_language(
        df_agg,
        "java",
        "95%",
        "P95 - Java",
        "java_p95.png",
        "P95 (ms)",
    )

    plot_metric_by_language(
        df_agg,
        "java",
        "Requests/s",
        "Requisições por Segundo - Java",
        "java_rps.png",
        "Requisições/s",
    )


    plot_metric_by_language(
        df_agg,
        "kotlin",
        "Average Response Time",
        "Latência Média - Kotlin",
        "kotlin_latencia_media.png",
        "Latência Média (ms)",
    )
    
    plot_metric_by_language(
        df_agg,
        "kotlin",
        "95%",
        "P95 - Kotlin",
        "kotlin_p95.png",
        "P95 (ms)",
    )
    
    plot_metric_by_language(
        df_agg,
        "kotlin",
        "Requests/s",
        "Requisições por Segundo - Kotlin",
        "kotlin_rps.png",
        "Requisições/s",
    )
    
    plot_error_rate_comparison(df)
    plot_error_rate_by_language(df,"java")
    plot_error_rate_by_language(df,"kotlin")

    print(
        f"Gráficos salvos em: {OUTPUT_DIR.resolve()}"
    )


if __name__ == "__main__":
    main()