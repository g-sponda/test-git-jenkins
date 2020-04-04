from prometheus_client.core import REGISTRY
from aws_dms_task_status_exporter.build_dms_status_exporter import AwsDmsReplicationTaskStatusCollector
from aws_dms_task_status_exporter.helper import clean_registry
from prometheus_client import make_wsgi_app
from wsgiref.simple_server import make_server


clean_registry()
REGISTRY.register(AwsDmsReplicationTaskStatusCollector())

app = make_wsgi_app()
httpd = make_server("", 9213, app)
httpd.serve_forever()
