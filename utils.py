import pandas as pd

def load_data(path="food_data.csv"):
    return pd.read_csv(path)
