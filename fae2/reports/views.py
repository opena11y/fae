from django.http import HttpResponse
from django.views.generic import TemplateView

class RunReport(TemplateView):
    template_name = 'reports/run_report.html'
