import pandas as pd

def calc_best_pool(df: pd.DataFrame, instance_type: str = None, az: str = None) -> str:
    """Calcula o melhor pool a partir de um DataFrame."""

    if instance_type:
        df = df[df["pool_id"].str.contains(instance_type)]
    
    if az:
        df = df[df["pool_id"].str.endswith(az)]
    
    if df.empty:
        return None
    
    stats = (
        df.groupby("pool_id")
        .apply(lambda g: (g["status"] == "SUCCESS").sum())
        .reset_index(name="success_count")
    )

    return stats.loc[stats["success_count"].idxmax(), "pool_id"]
