import argparse
import unittest
from unittest import mock
from aws_dms_task_status_exporter.build_dms_status_exporter import (
    AwsDmsReplicationTaskStatusCollector,
)
from prometheus_client.samples import Sample

mocked_response = [
    {"replication_task_identifier": "test1", "status": "failed"},
    {"replication_task_identifier": "test2", "status": "running"},
    {"replication_task_identifier": "test3", "status": "creating"},
    {"replication_task_identifier": "test4", "status": "stopped"},
    {"replication_task_identifier": "test5", "status": "stopping"},
    {"replication_task_identifier": "test6", "status": "deleting"},
    {"replication_task_identifier": "test7", "status": "starting"},
    {"replication_task_identifier": "test8", "status": "ready"},
    {"replication_task_identifier": "test9", "status": "modifying"},
]


class TestBuildDmsStatusExporterClass(unittest.TestCase):
    @mock.patch(
        "aws_dms_task_status_exporter.build_dms_status_exporter.get_status_replication_tasks",
        return_value=mocked_response,
    )
    def test_get_conf_file(self, get_status_replication_tasks):
        expected_response_sample = [
            Sample(
                "aws_dms_replication_task_status", {"replication_task_id": "test1"}, 0
            ),
            Sample(
                "aws_dms_replication_task_status", {"replication_task_id": "test2"}, 1
            ),
            Sample(
                "aws_dms_replication_task_status", {"replication_task_id": "test3"}, 2
            ),
            Sample(
                "aws_dms_replication_task_status", {"replication_task_id": "test4"}, 3
            ),
            Sample(
                "aws_dms_replication_task_status", {"replication_task_id": "test5"}, 4
            ),
            Sample(
                "aws_dms_replication_task_status", {"replication_task_id": "test6"}, 5
            ),
            Sample(
                "aws_dms_replication_task_status", {"replication_task_id": "test7"}, 6
            ),
            Sample(
                "aws_dms_replication_task_status", {"replication_task_id": "test8"}, 7
            ),
            Sample(
                "aws_dms_replication_task_status", {"replication_task_id": "test9"}, 8
            ),
        ]

        replication_task = AwsDmsReplicationTaskStatusCollector()
        result = next(replication_task.collect())

        assert result.samples == expected_response_sample
