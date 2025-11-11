import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from typing import Optimal

def plot_depreciacao_por_ano(df: pd.DataFrame, marca_modelo: str, modelo_regressao: Optional[LinearRegression] = None):

