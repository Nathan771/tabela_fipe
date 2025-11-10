import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from typing import Tuple, Dict, Any, Optional

def engenharia_de_features(df: pd.DataFrame, ano_referencia: int = 2025) -> pd.DataFrame:
    print(f" Criando novas features para o ano de referência: {ano_referencia}")
    df_features = df.copy()

    if 'Ano_Modelo' in df_features.columns:
        df_features['Idade_Carro'] = ano_referencia - df_features['Ano_Modelo']
        df_features['Idade_Carro'] = df_features['Idade_Carro'].apply(lambda x: max(0, x))
    else:
        print(" Coluna 'Ano_Modelo' não encontrada para engenharia de features.")
    
    return df_features

def treinar_modelo_depreciacao(df_features: pd.DataFrame) -> Optional[LinearRegression]:

    print(" Iniciando treinamento da Regressão Linear")

    if df_features.empty or 'Idade_Carro' not in df_features.columns or 'Valor_FIPE_Limpo' not in df_features.columns:
        print(" Erro: Dataframe sem as colunas necessárias.")
        return None
    
    x = df_features[['Idade_Carro']]
    y = df_features['Valor_FIPE_Limpo']

    
