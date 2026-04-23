from graficos import gerar_grafico
import pandas as pd

if __name__ == "__main__":
    df_testes = pd.read_csv("data/final.csv")

    print(df_testes.head(5))

    gerar_grafico(df_testes)