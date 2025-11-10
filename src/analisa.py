import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from typing import Tuple, Dict, Any, Optional

def engenharia_de_features(df: pd.DataFrame, ano_referencia: int = 2025) -> pd.DataFrame:
    