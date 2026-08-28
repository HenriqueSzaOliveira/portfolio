import pandas as pd
import boto3
import io
import os

def load_data(filepath: str = "jobs.json") -> pd.DataFrame:
    """
    Carrega dados de um arquivo ou de todos os arquivos JSON em um diretório.
    """
    if os.path.isdir(filepath):
        dfs = []
        for file in os.listdir(filepath):
            if file.endswith(".json"):
                full_path = os.path.join(filepath, file)
                dfs.append(pd.read_json(full_path, lines=True))
        return pd.concat(dfs, ignore_index=True)
    else:
        return pd.read_json(filepath, lines=True)

def load_data_s3(bucket: str, prefix: str = None, key: str = None) -> pd.DataFrame:
    """
    Carrega dados de um arquivo único ou de todos os arquivos sob um prefixo no S3.
    - Se 'key' for passado, lê apenas esse arquivo.
    - Se 'prefix' for passado, lê todos os arquivos sob esse prefixo.
    """
    s3 = boto3.client("s3")

    if key:
        obj = s3.get_object(Bucket=bucket, Key=key)
        data = obj["Body"].read().decode("utf-8")
        return pd.read_json(io.StringIO(data), lines=True)

    elif prefix:
        dfs = []
        response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
        for obj in response.get("Contents", []):
            key = obj["Key"]
            obj_data = s3.get_object(Bucket=bucket, Key=key)
            data = obj_data["Body"].read().decode("utf-8")
            dfs.append(pd.read_json(io.StringIO(data), lines=True))
        return pd.concat(dfs, ignore_index=True)

    else:
        raise ValueError("É necessário fornecer 'key' ou 'prefix' para leitura no S3.")