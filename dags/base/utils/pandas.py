import pandas as pd


def null_safe(value):
    return value if not pd.isnull(value) else None
