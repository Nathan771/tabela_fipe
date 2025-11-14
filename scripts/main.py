import sys
import os
import pandas as pd

caminho_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if caminho_raiz not in sys.path:
    sys.path.append(caminho_raiz)

from src.extrai import requisicao_e_loop_de_precos
from src.trat import limpar_e_converter_valores
from src.analisa import treinar_modelo_depreciacao
from src.visual import plot_depreciacao_por_ano


CODIGO_MARCA = '59'
CODIGO_MODELO = '5940'
DIRETORIO_RAW = 'data/raw'
DIRETORIO_PROCESSED = 'data/processed'

def garantir_diretorios():
    os.makedirs(DIRETORIO_RAW, exist_ok = True)
    os.makedirs(DIRETORIO_PROCESSED, exist_ok = True)

def rodar_pipeline():

    garantir_diretorios()

    print(f"Iniciando extração: Modelo {CODIGO_MODELO}")
    df_bruto = requisicao_e_loop_de_precos(CODIGO_MARCA, CODIGO_MODELO)

    if df_bruto is None or df_bruto.empty:
        print("Pipeline não executado: Não retornou os dados corretamente.")
        return
    

    caminho_bruto = os.path.join(DIRETORIO_RAW, 'fipe_dados_brutos.csv')
    df_bruto.to_csv(caminho_bruto, index = False, encoding = 'utf-8')
    print(f"Dados brutos salvos em: {caminho_bruto}")

    print("\n2. Iniciando tratamento de dados")
    df_limpo = limpar_e_converter_valores(df_bruto)

    if df_limpo is None:
        return
    
    caminho_limpo = os.path.join(DIRETORIO_PROCESSED, 'fipe_limpa.parquet')
    df_limpo.to_parquet(caminho_limpo, index = False)
    print(f" Dados limpos salvos em: {caminho_limpo}")

    print("\n Iniciando análise e modelagem.")

    modelo_depreciacao = treinar_modelo_depreciacao(df_limpo)

    print("\n Gerando visualizações.")

    plot_depreciacao_por_ano(df_limpo, f"VW Modelo {CODIGO_MODELO}")

    print("\n Pipeline concluído. ")


if __name__ == "__main__":
    rodar_pipeline()