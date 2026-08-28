import pandas as pd

from portfolio.APIRestSelectPoolsInstances.src.utils.pool_selector import calc_best_pool


def test_calc_best_pool_returns_pool_with_most_successes():
    data = pd.DataFrame(
        [
            {"pool_id": "pool-a", "status": "SUCCESS"},
            {"pool_id": "pool-a", "status": "FAILED"},
            {"pool_id": "pool-b", "status": "SUCCESS"},
            {"pool_id": "pool-b", "status": "SUCCESS"},
        ]
    )

    assert calc_best_pool(data) == "pool-b"


def test_calc_best_pool_applies_instance_type_and_az_filters():
    data = pd.DataFrame(
        [
            {"pool_id": "pool-r6.xlarge-us-east-1c", "status": "SUCCESS"},
            {"pool_id": "pool-r6.xlarge-us-east-1c", "status": "FAILED"},
            {"pool_id": "pool-c6.xlarge-us-east-1a", "status": "SUCCESS"},
            {"pool_id": "pool-c6.xlarge-us-east-1a", "status": "SUCCESS"},
        ]
    )

    assert calc_best_pool(data, "r6.xlarge", "us-east-1c") == "pool-r6.xlarge-us-east-1c"


def test_calc_best_pool_returns_none_when_filters_match_nothing():
    data = pd.DataFrame(
        [{"pool_id": "pool-r6.xlarge-us-east-1c", "status": "SUCCESS"}]
    )

    assert calc_best_pool(data, az="us-east-1a") is None
