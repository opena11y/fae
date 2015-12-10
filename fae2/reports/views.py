from html.parser import HTMLParser
from html.entities import name2codepoint

from django.http import HttpResponse 
from django.http import JsonResponse
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

    success_url = reverse_lazy('processing_reports')

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

class ProcessingStatusView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/processing.html'

    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return JsonResponse(self.get_data(context), **response_kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProcessingReportView, self).get_context_data(**kwargs)

        context['reports'] = WebsiteReport.objects.exclude(status='A').exclude(status='E')
        context['errors'] = WebsiteReport.objects.filter(status='E')
        
        return context    


class ArchivedReportView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/archived.html'

    def get_context_data(self, **kwargs):
        context = super(ArchivedReportView, self).get_context_data(**kwargs)

        context['reports'] = WebsiteReport.objects.filter(status='C')
        
        return context            

class ManageReportView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/manage.html'

    def get_context_data(self, **kwargs):
        context = super(ManageReportView, self).get_context_data(**kwargs)

        context['reports'] = WebsiteReport.objects.filter(status='C')
        
        return context                    

class ReportView(TemplateView):
    template_name = 'reports/report.html'

    def get_context_data(self, **kwargs):
        context = super(ReportView, self).get_context_data(**kwargs)

        view = kwargs['view']

        report = WebsiteReport.objects.get(slug=kwargs['report'])

        if view == 'gl':
          groups = report.ws_gl_results.all()
        elif view == 'rs':  
          groups = report.ws_rs_results.all()
        else:  
          groups = report.ws_rc_results.all()
          view = 'rc'

        context['report']   = report
        context['view']     = view
        context['summary']  = report
        context['groups']   = groups
        
        return context            

        

class ReportGroupView(TemplateView):
    template_name = 'reports/report_group.html'

    def get_context_data(self, **kwargs):
        context = super(ReportGroupView, self).get_context_data(**kwargs)

        view = kwargs['view']

        report = WebsiteReport.objects.get(slug=kwargs['report'])
        if view == 'gl':
          group = report.ws_gl_results.get(slug=kwargs['group'])
        elif view == 'rs':  
          group = report.ws_rs_results.get(slug=kwargs['group'])
        else:  
          group = report.ws_rc_results.get(slug=kwargs['group'])
          view = 'rc'

        context['report']  = report
        context['view']    = view
        context['summary'] = group
        context['group']   = group
        
        return context            

class ReportGroupRuleView(TemplateView):
    template_name = 'reports/report_group_rule.html'

    def get_context_data(self, **kwargs):
        context = super(ReportGroupRuleView, self).get_context_data(**kwargs)

        view = kwargs['view']

        report = WebsiteReport.objects.get(slug=kwargs['report'])
        if view == 'gl':
          group = report.ws_gl_results.get(slug=kwargs['group'])
        elif view == 'rs':  
          group = report.ws_rs_results.get(slug=kwargs['group'])
        else:  
          group = report.ws_rc_results.get(slug=kwargs['group'])
          view = 'rc'

        ws_rule_result = group.ws_rule_results.get(slug=kwargs['rule'])

        context['report']           = report
        context['view']             = view
        context['group']            = group
        context['summary']          = ws_rule_result
        context['ws_rule_result']      = ws_rule_result
        
        return context            


class ReportGroupRulePageView(TemplateView):
    template_name = 'reports/report_group_rule_page.html'

    def get_context_data(self, **kwargs):
        context = super(ReportGroupRulePageView, self).get_context_data(**kwargs)

        view = kwargs['view']

        report = WebsiteReport.objects.get(slug=kwargs['report'])
        if view == 'gl':
          group = report.ws_gl_results.get(slug=kwargs['group'])
        elif view == 'rs':  
          group = report.ws_rs_results.get(slug=kwargs['group'])
        else:  
          group = report.ws_rc_results.get(slug=kwargs['group'])
          view_opt = 'rc'

        ws_rule_result   = group.ws_rule_results.get(slug=kwargs['rule'])
        page_rule_result = ws_rule_result.page_rule_results.get(page_result__page_number=kwargs['page'])

        context['report']   = report
        context['view']     = view
        context['group']    = group
        context['summary']           = page_rule_result
        context['page_rule_result']  = page_rule_result
        context['result_messages']   = page_rule_result.result_message.split(';')        
        return context      

class ReportGroupRulePageElementResultsJSON(TemplateView):
    template_name = 'reports/report_group_rule_page.html'

    def get_context_data(self, **kwargs):
        context = super(ReportGroupRulePageView, self).get_context_data(**kwargs)

        view = kwargs['view']

        report = WebsiteReport.objects.get(slug=kwargs['report'])
        if view == 'gl':
          group = report.ws_gl_results.get(slug=kwargs['group'])
        elif view == 'rs':  
          group = report.ws_rs_results.get(slug=kwargs['group'])
        else:  
          group = report.ws_rc_results.get(slug=kwargs['group'])
          view_opt = 'rc'

        ws_rule_result   = group.ws_rule_results.get(slug=kwargs['rule'])
        page_rule_result = ws_rule_result.page_rule_results.get(page_result__page_number=kwargs['page'])

        context['report']   = report
        context['view']     = view
        context['group']    = group
        context['summary']           = page_rule_result
        context['page_rule_result']  = page_rule_result
        context['result_messages']   = page_rule_result.result_message.split(';')        
        return context    

class ReportPageView(TemplateView):
    template_name = 'reports/report_page.html'

    def get_context_data(self, **kwargs):
        context = super(ReportPageView, self).get_context_data(**kwargs)

        view = kwargs['view']

        report = WebsiteReport.objects.get(slug=kwargs['report'])
        page   = report.page_all_results.get(page_number=kwargs['page'])

        if view == 'gl':
          groups = page.page_gl_results.all()
        elif view == 'rs':  
          groups = page.page_rs_results.all()
        else:  
          groups = page.page_rc_results.all()
          view_opt = 'rc'


        context['report']        = report
        context['view']          = view
        context['summary']       = page
        context['groups']        = groups
        context['page']          = page
        
        return context            


class ReportPageGroupView(TemplateView):
    template_name = 'reports/report_page_group.html'

    def get_context_data(self, **kwargs):
        context = super(ReportPageGroupView, self).get_context_data(**kwargs)

        view = kwargs['view']

        report = WebsiteReport.objects.get(slug=kwargs['report'])
        page   = report.page_all_results.get(page_number=kwargs['page'])
        if view == 'gl':
          group = page.page_gl_results.get(slug=kwargs['group'])
        elif view == 'rs':  
          group = page.page_rs_results.get(slug=kwargs['group'])
        else:  
          group = page.page_rc_results.get(slug=kwargs['group'])
          view_opt = 'rc'

        context['report']   = report
        context['view']     = view
        context['summary']  = page
        context['group']    = group     
        context['page']     = page
        
        return context           

class ReportPageGroupRuleView(TemplateView):
    template_name = 'reports/report_page_group_rule.html'

    def get_context_data(self, **kwargs):
        context = super(ReportPageGroupRuleView, self).get_context_data(**kwargs)

        view = kwargs['view']

        report = WebsiteReport.objects.get(slug=kwargs['report'])
        page   = report.page_all_results.get(page_number=kwargs['page'])
        if view == 'gl':
          group = page.page_gl_results.get(slug=kwargs['group'])
        elif view == 'rs':  
          group = page.page_rs_results.get(slug=kwargs['group'])
        else:  
          group = page.page_rc_results.get(slug=kwargs['group'])
          view_opt = 'rc'

        page_rule_result = group.page_rule_results.get(slug=kwargs['rule'])

        context['report']        = report
        context['view']          = view
        context['summary']       = page
        context['group']         = group
        context['page']          = page
        context['page_rule_result'] = page_rule_result
        context['result_messages']   = page_rule_result.result_message.split(';')        

        
        return context             


class URLSummaryView(TemplateView):
    template_name = 'reports/report_url_summary.html'

    def get_context_data(self, **kwargs):
        context = super(ReportView, self).get_context_data(**kwargs)

        report = WebsiteReport.objects.get(slug=kwargs['slug'])

        context['report'] = report
        
        return context            
