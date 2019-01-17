from django.db import models
from django.core.validators import validate_ipv46_address
from apache_viewer.utils import format_date
from django.db.models import Sum, Count


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


class AggregateQuerySet(models.QuerySet):
    def total_size(self):
        """ Total size of all log requests"""
        return self.aggregate(total_size=Sum("request_size")).get("total_size", 0)

    def count_unique_ips(self):
        """ Get all unique IP """
        return self.aggregate(total_ip_count=Count("ip", distinct=True)).get(
            "total_ip_count", 0
        )

    def summary_ips_count(self):
        """ Group by IP and count """
        return self.values("ip").annotate(ip_count=Count("ip")).order_by("-ip_count")

    def summary_methods_count(self):
        """ Group by HTTP methods and count """
        return (
            self.values("request_method")
            .annotate(method_count=Count("request_method"))
            .order_by("-method_count")
        )


class Logs(models.Model):
    """
    Logs models
    """

    objects = LogsManager.from_queryset(AggregateQuerySet)()

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
        verbose_name = "logs"
