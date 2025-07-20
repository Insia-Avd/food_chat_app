import pandas as pd

def load_data(path="data/food_data.csv"):
    return pd.read_csv(path)
