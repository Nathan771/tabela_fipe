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

    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    modelo = LinearRegression()
    modelo.fit(X_train, y_train)

    y_pred = modelo.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    print(f" Modelo treinado com sucesso. RMSE: {rmse: 2f}, R2 Score: {r2:.2f}")
    print(f" Coeficiente de Depreciação (por ano de idade): R$ {modelo.coef_[0]:.2f}")
    print(f" Intercepto (valor base): R$ {modelo.intercept_:.2f}")


    return modelo

if __name__ == '__main__':

    print("Módulo 'analisa.py' testando engenharia de features e treinamento de modelo.")


    data = {
        'Modelo': ['Polo', 'Polo', 'Polo', 'Polo', 'Polo'],
        'Ano_Modelo': [2020, 2018, 2015, 2012, 2010],
        'Valor_FIPE_Limpo': [80000.0, 70000.0, 55000.0, 40000.0, 30000.0]

    }
    df_exemplo = pd.DataFrame(data)

    df_com_features = engenharia_de_features(df_exemplo, ano_referencia=2024)
    if df_com_features is not None:
        print("\nDataFrame com features: ")
        print(df_com_features.head())

        modelo_treinado = treinar_modelo_depreciacao(df_com_features)
        if modelo_treinado:
            print(f"\n Modelo treinado: {modelo_treinado}")