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


def main():
    df = load_data()

    df = aggregate(df)

    plot_avg_latency(df)
    plot_p95(df)
    plot_rps(df)

    print(
        f"Gráficos salvos em: {OUTPUT_DIR.resolve()}"
    )


if __name__ == "__main__":
    main()