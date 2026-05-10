import re
import pandas as pd
from pathlib import Path

pasta_raiz = Path("locust/resultados")

dfs = []

for arquivo in sorted(pasta_raiz.rglob("*_stats.csv")):
    if arquivo.name.endswith("_stats_history.csv"):
        continue

    partes = arquivo.parts

    # Pula pastas do trabalho 3 (instancia_X)
    if any(p.startswith("instancia_") for p in partes):
        continue

    df = pd.read_csv(arquivo)
    df = df[df["Name"] != "Aggregated"]

    carga_raw   = partes[2]
    cenario_raw = partes[3]

    linguagem_api = "Python" if "-py-" in cenario_raw else "Ruby"

    # Corrigido: sem-redis = False, com redis = True
    tem_redis = "sem-redis" not in cenario_raw

    match_usuarios = re.search(r"_(\d+)_\d+_stats\.csv$", arquivo.name)
    qtd_usuarios = int(match_usuarios.group(1)) if match_usuarios else None

    df["classe"]       = carga_raw
    df["qtd_usuarios"] = qtd_usuarios
    df["tem_redis"]    = tem_redis
    df["linguagem_api"] = linguagem_api
    df["cenario"]      = cenario_raw

    print(arquivo)
    dfs.append(df)

df_final = pd.concat(dfs, ignore_index=True)
df_final.to_csv("resultado_final_stats.csv", index=False)

print(f"\nFinalizado. {len(df_final)} linhas salvas em resultado_final_stats.csv")