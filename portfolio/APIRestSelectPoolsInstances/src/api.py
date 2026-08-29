from fastapi import FastAPI, Query
from pydantic import BaseModel
import time
from .utils.data_loader import load_data
from .utils.pool_selector import calc_best_pool

app = FastAPI(
    title="API Seleção de Pools EC2 Spot",
    description="API REST para selecionar o melhor pool de instâncias Spark considerando falhas de spot instances.",
    version="1.0.0"
)
cache = {}

class PoolResponse(BaseModel):
    best_pool: str

class ErrorResponse(BaseModel):
    error: str

@app.get("/get-pool",
         summary="Seleciona o melhor pool",
         description="Retorna o melhor pool de instâncias considerando filtros opcionais por tipo e AZ.",
         responses={
            200: {"model": PoolResponse, "description": "Resposta com o melhor pool"},
            404: {"model": ErrorResponse, "description": "Nenhum pool encontrado para os filtros"}
        })
def get_pool(
    instance_type: str = Query(None, description="Tipo de instância (ex: r6.xlarge)"),
    az: str = Query(None, description="Zona de disponibilidade (ex: us-east-1c)")
):
    """
    Endpoint que retorna o melhor pool de instâncias.
    - Filtro opcional por tipo de instância (`instance_type`)
    - Filtro opcional por zona de disponibilidade (`az`)
    """
    cache_key = f"{instance_type or 'all'}-{az or 'all'}"

    if cache_key not in cache or time.time() - cache[cache_key]["last_update"] > 5:
        df = load_data("./bucket/")
        best_pool = calc_best_pool(df, instance_type, az)
        cache[cache_key] = {"best_pool": best_pool, "last_update": time.time()}

    if not cache[cache_key]["best_pool"]:
        return {"error": "Não temos estatisticas suficientes para os filtros informados"}

    return {"best_pool": cache[cache_key]["best_pool"]}
