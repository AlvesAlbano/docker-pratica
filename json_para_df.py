from pathlib import Path
import json
import re

import numpy as np
import pandas as pd


OUTPUT_FILE = "grpc_stats.csv"

COLUMNS = [
    "carga",
    "linguagem",
    "tipo_api",
    "R",
    "usuarios",
    "Type",
    "Name",
    "Request Count",
    "Failure Count",
    "Median Response Time",
    "Average Response Time",
    "Min Response Time",
    "Max Response Time",
    "Average Content Size",
    "Requests/s",
    "Failures/s",
    "50%",
    "66%",
    "75%",
    "80%",
    "90%",
    "95%",
    "98%",
    "99%",
    "99.9%",
    "99.99%",
    "100%",
]


def extract_metadata(json_path: Path):
    """
    Exemplo:
    resultados-grpc/leve/api-grpc-java/api-grpc-java_musica_get_u100.json

    Retorna:
    - scenario: leve
    - language: java
    """

    scenario = json_path.parts[-3]

    implementation = json_path.parts[-2].lower()

    if "java" in implementation:
        language = "java"
    elif "kotlin" in implementation:
        language = "kotlin"
    else:
        language = implementation

    return scenario, language


def extract_file_metadata(json_path: Path):
    """
    Exemplo:
    api-grpc-java_musica_get_u100.json

    Retorna:
    - resource: musica
    - method: GET
    - users: 100
    """

    stem = json_path.stem

    match = re.search(
        r"_(musica|playlist|usuario)_(get|post)_u(\d+)$",
        stem,
        re.IGNORECASE,
    )

    if not match:
        raise ValueError(
            f"Não foi possível extrair metadados de {json_path.name}"
        )

    resource = match.group(1).lower()
    method = match.group(2).upper()
    users = int(match.group(3))

    return resource, method, users


def percentile(values, p):
    return float(np.percentile(values, p))


def ghz_json_to_row(json_file):
    json_file = Path(json_file)

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    scenario, language = extract_metadata(json_file)

    resource, method, users = extract_file_metadata(
        json_file
    )

    details = data.get("details", [])

    if not details:
        raise ValueError(
            f"O arquivo {json_file.name} não possui 'details'"
        )

    # ghz grava latência em nanossegundos
    latencies_ms = np.array(
        [d["latency"] / 1_000_000 for d in details],
        dtype=float,
    )

    failures = sum(
        1
        for d in details
        if d.get("status") != "OK"
    )

    duration_seconds = data["total"] / 1_000_000_000

    return {
        "carga": scenario,
        "linguagem": language,
        "tipo_api": "grpc",

        "R": resource,
        "usuarios": users,

        # Compatível com Locust
        "Type": method,
        "Name": data["options"]["call"],

        "Request Count": int(data["count"]),
        "Failure Count": int(failures),

        "Median Response Time": percentile(latencies_ms, 50),
        "Average Response Time": float(latencies_ms.mean()),
        "Min Response Time": float(latencies_ms.min()),
        "Max Response Time": float(latencies_ms.max()),

        "Average Content Size": 0,

        "Requests/s": float(data["rps"]),
        "Failures/s": float(
            failures / duration_seconds
        ),

        "50%": percentile(latencies_ms, 50),
        "66%": percentile(latencies_ms, 66),
        "75%": percentile(latencies_ms, 75),
        "80%": percentile(latencies_ms, 80),
        "90%": percentile(latencies_ms, 90),
        "95%": percentile(latencies_ms, 95),
        "98%": percentile(latencies_ms, 98),
        "99%": percentile(latencies_ms, 99),
        "99.9%": percentile(latencies_ms, 99.9),
        "99.99%": percentile(latencies_ms, 99.99),
        "100%": float(latencies_ms.max()),
    }


def build_dataframe(root_dir="resultados-grpc"):
    rows = []

    for json_file in Path(root_dir).rglob("*.json"):
        try:
            rows.append(
                ghz_json_to_row(json_file)
            )
            print(f"[OK] {json_file}")

        except Exception as e:
            print(
                f"[ERRO] {json_file}: {e}"
            )

    return pd.DataFrame(
        rows,
        columns=COLUMNS
    )


def main():
    df = build_dataframe(
        "resultados-grpc"
    )

    if df.empty:
        print(
            "Nenhum resultado encontrado."
        )
        return

    df = df.sort_values(
        by=[
            "carga",
            "linguagem",
            "R",
            "usuarios",
        ]
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8",
    )

    print("\n===================================")
    print("CSV gerado com sucesso")
    print("===================================")
    print(f"Arquivo: {OUTPUT_FILE}")
    print(f"Linhas: {len(df)}")
    print()

    print(df.head())


if __name__ == "__main__":
    main()