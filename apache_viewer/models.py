from django.db import models
from django.core.validators import validate_ipv46_address


class Logs(models.Model):
    """
    Logs models
    """

    ip = models.CharField(
        max_length=40, validators=[validate_ipv46_address], db_index=True
    )
    tms = models.DateTimeField()
    request_method = models.TextField(max_length=5)
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
