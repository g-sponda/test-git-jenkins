import argparse
import unittest
from unittest import mock
from aws_dms_task_status_exporter.helper import get_conf_file, clean_registry
from prometheus_client.core import REGISTRY


class TestHelperModule(unittest.TestCase):
    @mock.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(file="tests/test.yml"),
    )
    def test_get_conf_file(self, args):
        expected_dict = {
            "region": "us-east-1",
            "replication-task-id": [
                "task-id-1",
                "task-id-2",
                "task-id-3",
                "task-id-4",
                "task-id-5",
            ],
        }
        result_dict = get_conf_file()
        assert result_dict == expected_dict

    def test_clean_registry(self):
        initial_registry = REGISTRY._names_to_collectors.items()
        assert len(initial_registry) > 0

        clean_registry()
        cleaned_registry = REGISTRY._names_to_collectors.items()
        assert len(cleaned_registry) == 0
