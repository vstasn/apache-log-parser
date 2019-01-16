import django_filters
from .models import Logs


class ApacheLogFilter(django_filters.FilterSet):

    class Meta:
        model = Logs
        fields = [
            "ip",
            "tms",
            "request_method",
            "request_uri",
            "request_code",
            "request_size",
        ]
