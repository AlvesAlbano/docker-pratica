from pathlib import Path
import pandas as pd
import re

# Diretório raiz dos resultados
BASE_DIR = Path("locust/resultados")

# Lista para armazenar os DataFrames
dfs = []

# Procura todos os arquivos *_stats.csv
for arquivo in BASE_DIR.rglob("*_stats.csv"):

    nome = arquivo.stem

    # Exemplo esperado:
    # api-rest-kotlin_pesado_u300_r45_stats
    padrao = (
        r"api-(rest|graphql|soap|grpc)-"
        r"(java|kotlin)_"
        r"(leve|medio|pesado)_"
        r"u(\d+)_r(\d+)_stats"
    )

    match = re.match(padrao, nome)

    if not match:
        print(f"[AVISO] Arquivo ignorado: {arquivo}")
        continue

    tipo_api, linguagem, carga, usuarios, spawn_rate = match.groups()

    try:
        df = pd.read_csv(arquivo)

        # Adiciona metadados
        df["linguagem"] = linguagem
        df["tipo_api"] = tipo_api
        df["carga"] = carga
        df["usuarios"] = int(usuarios)      # U
        df["spawn_rate"] = int(spawn_rate)  # R

        dfs.append(df)

        print(f"[OK] {arquivo}")

    except Exception as e:
        print(f"[ERRO] {arquivo}: {e}")

# Verifica se encontrou arquivos
if not dfs:
    raise RuntimeError("Nenhum arquivo *_stats.csv encontrado.")

# Junta tudo
resultado = pd.concat(dfs, ignore_index=True)

# Reorganiza as colunas para deixar os metadados primeiro
colunas_metadados = [
    "linguagem",
    "tipo_api",
    "carga",
    "usuarios",
    "spawn_rate",
]

outras_colunas = [
    c for c in resultado.columns
    if c not in colunas_metadados
]

resultado = resultado[colunas_metadados + outras_colunas]

# Salva o CSV consolidado
arquivo_saida = "csv_junto.csv"
resultado.to_csv(arquivo_saida, index=False)

print("\n========================================")
print("Consolidação concluída com sucesso!")
print(f"Arquivos processados: {len(dfs)}")
print(f"Total de linhas: {len(resultado)}")
print(f"Arquivo gerado: {arquivo_saida}")
print("========================================")