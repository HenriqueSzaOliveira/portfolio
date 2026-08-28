import json
from unittest.mock import Mock, patch

import pandas as pd
import pytest

from portfolio.APIRestSelectPoolsInstances.src.utils.data_loader import (
    load_data,
    load_data_s3,
)


def test_load_data_reads_jsonl_file(tmp_path):
    path = tmp_path / "jobs.json"
    records = [
        {"job_id": "job-1", "pool_id": "pool-a", "status": "SUCCESS"},
        {"job_id": "job-2", "pool_id": "pool-b", "status": "FAILED"},
    ]
    path.write_text("\n".join(json.dumps(record) for record in records), encoding="utf-8")

    result = load_data(str(path))

    expected = pd.DataFrame(records)
    pd.testing.assert_frame_equal(result, expected)


def test_load_data_reads_all_json_files_from_directory(tmp_path):
    first = {"job_id": "job-1", "pool_id": "pool-a", "status": "SUCCESS"}
    second = {"job_id": "job-2", "pool_id": "pool-b", "status": "SUCCESS"}
    (tmp_path / "first.json").write_text(json.dumps(first), encoding="utf-8")
    (tmp_path / "second.json").write_text(json.dumps(second), encoding="utf-8")
    (tmp_path / "ignored.txt").write_text("not json", encoding="utf-8")

    result = load_data(str(tmp_path))

    assert set(result["job_id"]) == {"job-1", "job-2"}
    assert set(result["pool_id"]) == {"pool-a", "pool-b"}


def test_load_data_s3_reads_single_object():
    client = Mock()
    client.get_object.return_value = {
        "Body": Mock(read=Mock(return_value=b'{"job_id":"job-1","pool_id":"pool-a"}'))
    }

    with patch(
        "portfolio.APIRestSelectPoolsInstances.src.utils.data_loader.boto3.client",
        return_value=client,
    ):
        result = load_data_s3("bucket", key="logs/job-1.json")

    assert result.iloc[0]["job_id"] == "job-1"
    client.get_object.assert_called_once_with(Bucket="bucket", Key="logs/job-1.json")


def test_load_data_s3_reads_objects_from_prefix():
    client = Mock()
    client.list_objects_v2.return_value = {
        "Contents": [{"Key": "logs/first.json"}, {"Key": "logs/second.json"}]
    }
    client.get_object.side_effect = [
        {"Body": Mock(read=Mock(return_value=b'{"job_id":"job-1","pool_id":"pool-a"}'))},
        {"Body": Mock(read=Mock(return_value=b'{"job_id":"job-2","pool_id":"pool-b"}'))},
    ]

    with patch(
        "portfolio.APIRestSelectPoolsInstances.src.utils.data_loader.boto3.client",
        return_value=client,
    ):
        result = load_data_s3("bucket", prefix="logs/")

    assert list(result["job_id"]) == ["job-1", "job-2"]
    client.list_objects_v2.assert_called_once_with(Bucket="bucket", Prefix="logs/")


def test_load_data_s3_requires_key_or_prefix():
    with patch(
        "portfolio.APIRestSelectPoolsInstances.src.utils.data_loader.boto3.client"
    ):
        with pytest.raises(ValueError, match="key.*prefix"):
            load_data_s3("bucket")
