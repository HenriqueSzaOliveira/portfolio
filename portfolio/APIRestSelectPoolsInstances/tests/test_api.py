import pandas as pd

from portfolio.APIRestSelectPoolsInstances.src import api


def test_get_pool_returns_best_pool_with_filters(monkeypatch):
    data = pd.DataFrame(
        [
            {"pool_id": "pool-r6.xlarge-us-east-1c", "status": "SUCCESS"},
            {"pool_id": "pool-c6.xlarge-us-east-1a", "status": "SUCCESS"},
            {"pool_id": "pool-c6.xlarge-us-east-1a", "status": "SUCCESS"},
        ]
    )
    api.cache.clear()
    monkeypatch.setattr(api, "load_data", lambda _: data)

    result = api.get_pool(instance_type="c6.xlarge", az="us-east-1a")

    assert result == {"best_pool": "pool-c6.xlarge-us-east-1a"}


def test_get_pool_uses_cached_result(monkeypatch):
    data = pd.DataFrame(
        [{"pool_id": "pool-a", "status": "SUCCESS"}]
    )
    load_calls = []
    api.cache.clear()
    monkeypatch.setattr(
        api,
        "load_data",
        lambda path: (load_calls.append(path), data)[1],
    )

    assert api.get_pool(None, None) == {"best_pool": "pool-a"}
    assert api.get_pool(None, None) == {"best_pool": "pool-a"}

    assert len(load_calls) == 1


def test_get_pool_refreshes_expired_cache(monkeypatch):
    data = pd.DataFrame(
        [{"pool_id": "pool-refreshed", "status": "SUCCESS"}]
    )
    api.cache.clear()
    api.cache["all-all"] = {"best_pool": "pool-old", "last_update": 0}
    monkeypatch.setattr(api, "load_data", lambda _: data)
    monkeypatch.setattr(api.time, "time", lambda: 10)

    assert api.get_pool(None, None) == {"best_pool": "pool-refreshed"}
