from fastapi import FastAPI, Query
import time
from .utils.data_loader import load_data
from .utils.pool_selector import calc_best_pool

app = FastAPI()
cache = {}

@app.get("/get-pool")
def get_pool(instance_type: str = Query(None), az: str = Query(None)):
    cache_key = f"{instance_type or 'all'}-{az or 'all'}"

    if cache_key not in cache or time.time() - cache[cache_key]["last_update"] > 5:
        df = load_data("./bucket/")
        best_pool = calc_best_pool(df, instance_type, az)
        cache[cache_key] = {"best_pool": best_pool, "last_update": time.time()}

    return {"best_pool": cache[cache_key]["best_pool"]}