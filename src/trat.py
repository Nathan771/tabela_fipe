# src/trata.py

import pandas as pd
import numpy as np
from typing import Optional

def limpar_e_converter_valores(df: pd.DataFrame) -> Optional[pd.DataFrame]: # Limpa e transforma o DataFrame bruto, convertendo valores monetários e extraindo dados da string de ano/versão.

    if df.empty:
        print("Tratamento abortado: DataFrame de entrada está vazio.")
        return None
    
    print("Iniciando limpeza e conversão de valores...")
    
    df_tratado = df.copy()

    # 1. TRATAMENTO DO VALOR FIPE (R$ X.XXX,XX -> Número Float)
    if 'Valor_FIPE_Bruto' in df_tratado.columns:
        df_tratado['Valor_FIPE_Limpo'] = (
            df_tratado['Valor_FIPE_Bruto']
            .astype(str)
            .str.replace('R$', '', regex=False)
            .str.replace('.', '', regex=False) 
            .str.replace(',', '.', regex=False)
            .str.strip()
            .astype(float)
        )
        df_tratado = df_tratado.drop(columns=['Valor_FIPE_Bruto'])
    
    # 2. EXTRAÇÃO DE DADOS DA STRING DE ANO/VERSÃO
    if 'Ano/Versão_Bruto' in df_tratado.columns:
        # Extrai o Ano do Modelo
        df_tratado['Ano_Modelo'] = df_tratado['Ano/Versão_Bruto'].str.extract(r'(\d{4})').astype(float)
        
        # Extrai o Tipo de Combustível
        df_tratado['Combustivel'] = df_tratado['Ano/Versão_Bruto'].str.extract(r'(\w+)$')
        
        df_tratado = df_tratado.drop(columns=['Ano/Versão_Bruto'])

    print("Limpeza concluída.")
    return df_tratado