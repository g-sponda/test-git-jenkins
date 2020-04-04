import argparse
import datetime
import boto3
from botocore.stub import Stubber
import unittest
from unittest import mock
from aws_dms_task_status_exporter.aws import get_status_replication_tasks


class TestAwsModule(unittest.TestCase):
    _mocked_conf_file = {
        "region": "us-east-1",
        "replication-task-id": [
            "task-id-1",
            "task-id-2",
            "task-id-3",
            "task-id-4",
            "task-id-5",
        ],
    }

    @mock.patch(
        "aws_dms_task_status_exporter.aws.get_conf_file", return_value=_mocked_conf_file
    )
    def test_get_conf_file(self, get_conf_file):
        conf = get_conf_file()
        dms = boto3.client("dms", 'us-east-1')
        stubber = Stubber(dms)

        describe_replication_tasks_response = {
            "ReplicationTasks": [
                {"ReplicationTaskIdentifier": "test1", "Status": "failed"},
                {"ReplicationTaskIdentifier": "test2", "Status": "running"},
                {"ReplicationTaskIdentifier": "test3", "Status": "creating"},
                {"ReplicationTaskIdentifier": "test4", "Status": "stopped"},
                {"ReplicationTaskIdentifier": "test5", "Status": "stopping"},
                {"ReplicationTaskIdentifier": "test6", "Status": "deleting"},
                {"ReplicationTaskIdentifier": "test7", "Status": "starting"},
                {"ReplicationTaskIdentifier": "test8", "Status": "ready"},
                {"ReplicationTaskIdentifier": "test9", "Status": "modifying"},
            ]
        }

        expected_response = [
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

        stubber.add_response(
            "describe_replication_tasks", describe_replication_tasks_response
        )

        stubber.activate()
        resp = get_status_replication_tasks(dms_client=dms)
        stubber.deactivate()

        assert resp == expected_response
