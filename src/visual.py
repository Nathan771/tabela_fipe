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

    plt.title(f"Depreciação de preços - {marca_modelo} ao Longo dos Anos", fontsize = 16)
    plt.xlabel('Ano do Modelo', fontsize = 12)
    plt.ylabel('Valor FIPE (R$)', fontsize = 12)
    plt.grid(True, linestyle = '--', alpha = 0.6)
    plt.legend()
    plt.gca().ticklabel_format(style = 'plain', axis = 'y')
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    print("Módulo 'visual.py' testando plotagem.")

    data = {
        'Modelo': ['Polo', 'Polo', 'Polo', 'Polo', 'Polo'],
        'Ano_Modelo': [2020, 2018, 2015, 2012, 2010],
        'Valor_FIPE_Limpo': [80000.0, 70000.0, 55000.0, 40000.0, 30000.0],
        'Idade_Carro': [5, 7, 10, 13, 15] 
    }
    df_exemplo = pd.DataFrame(data)

    from sklearn.linear_model import LinearRegression
    modelo_dummy = LinearRegression()
    modelo_dummy.coef_ = [-5000]
    modelo_dummy.intercept_ = 100000

    plot_depreciacao_por_ano(df_exemplo, "Polo(Exemplo)", modelo_dummy)
    