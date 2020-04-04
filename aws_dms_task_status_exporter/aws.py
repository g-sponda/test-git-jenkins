from aws_dms_task_status_exporter.helper import get_conf_file
import boto3
from os import environ


def get_status_replication_tasks(dms_client=None):
    conf = get_conf_file()

    if not dms_client:
        dms_client = boto3.client(
            "dms",
            aws_access_key_id=environ.get("AWS_ACCESS_KEY", default=None),
            aws_secret_access_key=environ.get("AWS_SECRET_KEY", default=None),
            region_name=environ.get("AWS_REGION", default=conf["region"]),
        )

    result = []
    response = dms_client.describe_replication_tasks(
        Filters=[{"Name": "replication-task-id", "Values": conf["replication-task-id"]}]
    )["ReplicationTasks"]

    for resp in response:
        result.append(
            {
                "replication_task_identifier": resp["ReplicationTaskIdentifier"],
                "status": resp["Status"],
            }
        )

    return result
