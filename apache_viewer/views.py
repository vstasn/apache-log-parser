from django_filters.views import BaseFilterView
from django.views.generic import ListView
from apache_viewer.models import Logs
from .filters import ApacheLogFilter
import csv
from django.http import HttpResponse


def export_csv_file(queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment;filename=export.csv"
    field_names = [field.name for field in queryset.model._meta.fields]

    writer = csv.writer(response)
    writer.writerow(field_names)
    for row in queryset:
        writer.writerow([getattr(row, field) for field in field_names])
    return response


class LogsList(BaseFilterView, ListView):
    model = Logs
    paginate_by = 20
    template_name = "logs_list.html"
    filter_class = ApacheLogFilter
    # on startup filter is None, show all data
    strict = False

    def paginate_queryset(self, queryset, page_size):
        self.total_size = queryset.total_size()
        self.total_ip_count = queryset.count_unique_ips()
        self.total_ip_top10 = queryset.summary_ips_count()[:10]
        self.total_methods_top = queryset.summary_methods_count()

        return super().paginate_queryset(queryset, page_size)

    def get(self, request, *args, **kwargs):
        response = super().get(self, request, *args, **kwargs)

        format = self.request.GET.get("format", False)

        # url/?format=csv
        if format == "csv":
            return export_csv_file(self.object_list)

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # add aggregated data
        context["total_size"] = self.total_size
        context["total_ip_count"] = self.total_ip_count
        context["total_ip_top10"] = self.total_ip_top10
        context["total_methods_top"] = self.total_methods_top
        return context
