import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from typing import Optimal

def plot_depreciacao_por_ano(df: pd.DataFrame, marca_modelo: str, modelo_regressao: Optional[LinearRegression] = None):

    if df.empty:
        print(" Dataframe vazio")
        return
    
    print(f" Gerando gráfico de depreciação para {marca_modelo}")

    plt.figure(figsize=(10, 6))

    sns.scatterplot(
        x='Ano_Modelo',
        y='Valor_FIPE_Limpo',
        data=df,
        s=100,
        color='blue',
        alpha=0.7,
        label='Valores Reais'

)

    if modelo_regressao and 'Idade_Carro' in df.columns:
        min_idade = df['Idade_Carro'].min()
        max_idade = df['Idade_Carro'].max()

        idade_para_prever = pd.DataFrame({'Idade_Carro': range(int(min_idade), int(max_idade) + 1)})
        precos_previstos = modelo_regressao.predict(idade_para_prever)

        ano_atual = df['Ano_Modelo'].max() + df['Idade_Carro'].min()
        anos_previstos = ano_atual - idade_para_prever['Idade_Carro']

        sns.lineplot(
        x=anos_previstos,
        y=precos_previstos,
        color='green',
        linestyle='--',
        label='Linha de Regressão'
        )

        