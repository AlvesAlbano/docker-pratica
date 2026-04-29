import pandas as pd
from pathlib import Path

pasta_raiz = Path("locust/resultados")

dfs = []

for arquivo in pasta_raiz.rglob("*_stats.csv"):
    print(arquivo)
    df = pd.read_csv(arquivo)

    # remove Aggregated
    # descomenta para pegar os aggregated
    df = df[df["Name"] != "Aggregated"]

    partes = arquivo.parts

    classe = partes[2]
    instancia = int(partes[3].split("_")[1])
    tipo_execucao = "hibrido" if partes[4] == "todos" else "individual"

    nome = arquivo.stem
    qtd_usuarios = int([p for p in nome.split("_") if p.isdigit()][0])

    df["classe"] = classe
    df["instancias"] = instancia
    df["tipo_execucao"] = tipo_execucao
    df["qtd_usuarios"] = qtd_usuarios

    dfs.append(df)

df_final = pd.concat(dfs, ignore_index=True)

df_final.to_csv("resultado_final_stats.csv", index=False)