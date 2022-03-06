import pandas as pd

def df_val_map(df: pd.DataFrame, col: str, mapping:  dict) -> None:
    """For a given column, map values from one value to the other,
     defined in a mapping dict"""
    df[col] = df[col].map(mapping)