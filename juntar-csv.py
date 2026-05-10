import pandas as pd
from pathlib import Path

pasta_raiz = Path("locust/resultados")

dfs = []

for arquivo in pasta_raiz.rglob("*_stats.csv"):
    print(arquivo)
    df = pd.read_csv(arquivo)

    # remove Aggregated
    # comenta para pegar os aggregated
    df = df[df["Name"] != "Aggregated"]

    partes = arquivo.parts

    classe = partes[2]
    # instancia = int(partes[3].split("_")[1])
    redis = partes[3]
    linguagem_api = partes[3].split("-")[1]
    bp = 0

    if "sem-redis" in redis:
        tem_redis = True
    else:
        tem_redis = False

    if linguagem_api == "py":
        tipo_linguagem = "Python"
    else:
        tipo_linguagem = "Ruby"

    nome = arquivo.stem
    qtd_usuarios = int([p for p in nome.split("_") if p.isdigit()][0])

    df["classe"] = classe
    df["qtd_usuarios"] = qtd_usuarios
    df["tem_redis"] = tem_redis
    df["linguagem_api"] = tipo_linguagem

    dfs.append(df)

df_final = pd.concat(dfs, ignore_index=True)

df_final.to_csv("resultado_final_stats.csv", index=False)