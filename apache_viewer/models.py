from django.db import models
from django.core.validators import validate_ipv46_address
from apache_viewer.utils import format_date


REQUEST_METHODS_CHOICES = (
    ("post", "POST"),
    ("get", "GET"),
    ("head", "HEAD"),
    ("options", "OPTIONS"),
    ("trace", "TRACE"),
    ("connect", "CONNECT"),
    ("delete", "DELETE"),
    ("put", "PUT"),
)


class LogsManager(models.Manager):
    """
    Logs manager
    add methods to model
    """

    def create_logs_bulk(self, objects, batch_size=1000):
        return Logs.objects.bulk_create(objects, batch_size)

    def add_log_bulk(self, data):
        http_method = data["request_method"].lower()
        if http_method not in dict(REQUEST_METHODS_CHOICES):
            return False

        log_entry = Logs(
            ip=data["ip"],
            tms=format_date(data["time"]),
            request_method=http_method,
            request_uri=data["path"],
            request_code=int(data["status"]),
            request_size=int(data["bytes"]),
        )
        return log_entry


class Logs(models.Model):
    """
    Logs models
    """

    objects = LogsManager()

    ip = models.CharField(
        max_length=40, validators=[validate_ipv46_address], db_index=True
    )
    tms = models.DateTimeField()
    request_method = models.CharField(max_length=7, choices=REQUEST_METHODS_CHOICES)
    request_uri = models.TextField()
    request_code = models.IntegerField()
    request_size = models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=["request_method"]),
            models.Index(fields=["request_uri"]),
            models.Index(fields=["request_code"]),
            models.Index(fields=["request_size"]),
        ]
