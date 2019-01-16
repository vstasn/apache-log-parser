from django.db.models import Sum, Count
from django_filters.views import FilterView
from apache_viewer.models import Logs
from .filters import ViewFilter


class LogsList(FilterView):
    model = Logs
    paginate_by = 100
    template_name = "logs_list.html"

    filter_class = ViewFilter

    def paginate_queryset(self, queryset, page_size):
        self.result_total_size = queryset.aggregate(total_size=Sum("request_size"))[
            "total_size"
        ]
        self.result_ip_unique_count = queryset.aggregate(
            ip_unique_count=Count("ip", distinct=True)
        )["ip_unique_count"]
        self.result_ip_top_10 = (
            queryset.values("ip")
            .annotate(ip_count=Count("ip"))
            .order_by("-ip_count")[:10]
        )
        self.result_methods_top = (
            queryset.values("request_method")
            .annotate(method_count=Count("request_method"))
            .order_by("-method_count")
        )
        return super().paginate_queryset(queryset, page_size)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # add aggregated data
        context["total_size"] = self.result_total_size
        context["ip_unique_count"] = self.result_ip_unique_count
        context["ip_top_10"] = self.result_ip_top_10
        context["methods_top"] = self.result_methods_top
        return context
