from django.http import HttpResponse
from django.views.generic import TemplateView, CreateView, FormView
from reports.models import WebsiteReport
from django.core.urlresolvers import reverse_lazy
from braces.views import LoginRequiredMixin
from .uid import generate


class RunAnonymousReportView(CreateView):
    model = WebsiteReport
    fields = ['url', 'ruleset']
    template_name = 'reports/run_anonymous_report.html'

    success_url = reverse_lazy('processing_anonymous_report')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.slug = generate()
        return super(RunReportView, self).form_valid(form)

class RunReportView(LoginRequiredMixin, CreateView):
    model = WebsiteReport
    fields = ['url', 'title', 'depth', 'follow', 'ruleset']
    template_name = 'reports/run_report.html'

    success_url = reverse_lazy('processing_report')

    login_url = reverse_lazy('run_anonymous_report')
    redirect_field_name = "Anonymous Report"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.slug = generate()

        return super(RunReportView, self).form_valid(form)

class ProcessingReportView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/processing.html'

    def get_context_data(self, **kwargs):
        context = super(ProcessingReportView, self).get_context_data(**kwargs)

        context['reports'] = WebsiteReport.objects.exclude(status='A').exclude(status='E')
        context['errors'] = WebsiteReport.objects.filter(status='E')
        
        return context    

class ArchivedReportView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/archived.html'

    def get_context_data(self, **kwargs):
        context = super(ArchivedReportView, self).get_context_data(**kwargs)

        context['reports'] = WebsiteReport.objects.filter(status='A')
        
        return context            

class ManageReportView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/manage.html'

    def get_context_data(self, **kwargs):
        context = super(ManageReportView, self).get_context_data(**kwargs)

        context['reports'] = WebsiteReport.objects.filter(status='A')
        
        return context                    

class ReportView(TemplateView):
    template_name = 'reports/report.html'

    def get_context_data(self, **kwargs):
        context = super(ArchivedReportView, self).get_context_data(**kwargs)

        context['report'] = WebsiteReport.objects.get(slug=kwargs['slug'])
        
        return context            
