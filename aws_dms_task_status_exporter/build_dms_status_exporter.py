from aws_dms_task_status_exporter.aws import get_status_replication_tasks
from prometheus_client import Histogram
from prometheus_client.core import GaugeMetricFamily

states = {
    "failed": 0,
    "running": 1,
    "creating": 2,
    "stopped": 3,
    "stopping": 4,
    "deleting": 5,
    "starting": 6,
    "ready": 7,
    "modifying": 8,
}


class AwsDmsReplicationTaskStatusCollector:
    def collect(self):
        result = get_status_replication_tasks()
        c = GaugeMetricFamily(
            "aws_dms_replication_task_status",
            "Status of AWS DMS replication task",
            labels=["replication_task_id"],
        )
        for res in result:
            c.add_metric([res["replication_task_identifier"]], states[res["status"]])

        yield c
