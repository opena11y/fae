# from html.parser import HTMLParser
# from html.entities import name2codepoint

from django.http import HttpResponse 
from django.http import JsonResponse

from django.views.generic import TemplateView
from django.views.generic import CreateView 
from django.views.generic import FormView 
from django.views.generic import RedirectView

from django.contrib.auth.models import User

from reports.models import WebsiteReport
from userProfiles.models import UserProfile

from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .uid import generate

# ==============================================================
#
# Anonymous Run Report Views
#
# ==============================================================

class RunAnonymousReportView(CreateView):
    model = WebsiteReport
    fields = ['url', 'ruleset']
    template_name = 'reports/run_anonymous_report.html'

    success_url = reverse_lazy('processing_anonymous_reports')

    def form_valid(self, form):
        form.instance.user = User.objects.get(username='anonymous')
        form.instance.depth = 1
        form.instance.slug = generate()

        self.request.session['fae2_anonymous_slug'] = form.instance.slug
 
        return super(RunAnonymousReportView, self).form_valid(form)


class ProcessingAnonymousReportView(TemplateView):
    template_name = 'reports/processing_anonymous.html'

    def get_context_data(self, **kwargs):
        context = super(ProcessingAnonymousReportView, self).get_context_data(**kwargs)

        try:
          report  = WebsiteReport.objects.get(slug=self.request.session['fae2_anonymous_slug'])
        except:
          report = False

        context['report'] = report
        
        return context    

# ==============================================================
#
# Authenticated Report Views
#
# ==============================================================

class RunReportView(LoginRequiredMixin, CreateView):
    model = WebsiteReport
    fields = ['url', 'title', 'depth', 'follow', 'ruleset', 'max_pages']
    template_name = 'reports/run_report.html'

    success_url = reverse_lazy('processing_reports')

    login_url = reverse_lazy('run_anonymous_report')
    redirect_field_name = "Anonymous Report"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.slug = generate()

        return super(RunReportView, self).form_valid(form)

    def form_invalid(self, form):

        return super(RunReportView, self).form_invalid(form)

class ProcessingReportView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/processing.html'

    def get_context_data(self, **kwargs):
        context = super(ProcessingReportView, self).get_context_data(**kwargs)

        user_reports = WebsiteReport.objects.filter(user=self.request.user)

        context['reports'] = user_reports.exclude(status='A').exclude(status='E')
        context['errors']  = user_reports.filter(status='E')
        
        return context    

class ProcessingStatusAllJSON(LoginRequiredMixin, TemplateView):

    def render_to_response(self, context, **response_kwargs):

        json = []

        for r in context['reports']:
            json.append(r.toJSON())

        return  JsonResponse(json, safe=False, **response_kwargs)


    def get_context_data(self, **kwargs):
        context = super(ProcessingStatusAllJSON, self).get_context_data(**kwargs)

        user_reports = WebsiteReport.objects.filter(user=self.request.user)

        context['reports'] = user_reports.all()
        
        return context    

class ProcessingStatusJSON(TemplateView):

    def render_to_response(self, context, **response_kwargs):

        return  JsonResponse(context['report'].toJSON(), safe=False, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProcessingStatusJSON, self).get_context_data(**kwargs)

        report = WebsiteReport.objects.get(slug=kwargs['report'])

        context['report'] = report
        
        return context    

class SetReportArchiveView(TemplateView):

    def render_to_response(self, context, **response_kwargs):

        return  JsonResponse(context['report'].toJSON(), safe=False, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = super(SetReportArchiveView, self).get_context_data(**kwargs)

        report = WebsiteReport.objects.get(slug=kwargs['report'])
        value = kwargs['value']

        if value == 'true':
            report.archive = True
        else:    
            report.archive = False

        report.save()    

        context['report'] = report
        
        return context


class ArchivedReportView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/archived.html'

    def get_context_data(self, **kwargs):
        context = super(ArchivedReportView, self).get_context_data(**kwargs)

        user_reports = WebsiteReport.objects.filter(user=self.request.user)

        context['reports'] = user_reports.filter(status='C')
        context['profile'] = UserProfile.objects.get(user=self.request.user)
        
        return context            

class ManageReportView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/manage.html'

    def get_context_data(self, **kwargs):
        context = super(ManageReportView, self).get_context_data(**kwargs)

        user_reports = WebsiteReport.objects.filter(user=self.request.user)

        context['reports'] = user_reports.filter(status='C')
        
        return context                 


# ==============================================================
#
# Report Views
#
# ==============================================================

class ReportView(TemplateView):
    template_name = 'reports/report.html'

    def get_context_data(self, **kwargs):
        context = super(ReportView, self).get_context_data(**kwargs)

        view = kwargs['view']

        report = WebsiteReport.objects.get(slug=kwargs['report'])
        page = False

        if report.page_count == 1:
          page = report.get_first_page()
          if view == 'gl':
            groups = page.page_gl_results.all()
          elif view == 'rs':  
            groups = page.page_rs_results.all()
          else:  
            groups = page.page_rc_results.all()
            view = 'rc'
        else:
          if view == 'gl':
            groups = report.ws_gl_results.all()
          elif view == 'rs':  
            groups = report.ws_rs_results.all()
          else:  
            groups = report.ws_rc_results.all()
            view = 'rc'

        self.request.session['last_report_slug'] = report.slug
        self.request.session['last_report_view'] = view
        self.request.session['last_report_page_count'] = report.page_count

        context['page']     = page
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
          group        = report.ws_gl_results.get(slug=kwargs['group'])
          page_results = group.page_gl_results.all()
        elif view == 'rs':  
          group        = report.ws_rs_results.get(slug=kwargs['group'])
          page_results = group.page_rs_results.all()
        else:  
          group        = report.ws_rc_results.get(slug=kwargs['group'])
          page_results = group.page_rc_results.all()
          view = 'rc'

        self.request.session['last_report_slug'] = report.slug
        self.request.session['last_report_view'] = view
        self.request.session['last_report_page_count'] = report.page_count

        context['report']       = report
        context['view']         = view
        context['summary']      = group
        context['group']        = group
        context['page_results'] = page_results
        
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

        self.request.session['last_report_slug'] = report.slug
        self.request.session['last_report_view'] = view
        self.request.session['last_report_page_count'] = report.page_count

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

        view  = kwargs['view']
        group = kwargs['group']
        rule  = kwargs['rule']
        page  = kwargs['page']

        report = WebsiteReport.objects.get(slug=kwargs['report'])
        if view == 'gl':
          group = report.ws_gl_results.get(slug=group)
        elif view == 'rs':  
          group = report.ws_rs_results.get(slug=group)
        else:  
          group = report.ws_rc_results.get(slug=group)
          view_opt = 'rc'

        ws_rule_result   = group.ws_rule_results.get(slug=rule)
        page_rule_result = ws_rule_result.page_rule_results.get(page_result__page_number=kwargs['page'])

        self.request.session['last_report_slug'] = report.slug
        self.request.session['last_report_view'] = view
        self.request.session['last_report_page_count'] = report.page_count

        report.update_last_page_numbers(page_rule_result.page_result.page_number)

        self.request.session['last_report_slug'] = report.slug
        self.request.session['last_report_view'] = view
        self.request.session['last_report_page_count'] = report.page_count

        self.request.session['last_page_number']   = report.last_page
        self.request.session['last_prev_page_url']  = ""
        self.request.session['last_next_page_url']  = ""
        self.request.session['last_first_page_url'] = ""
        self.request.session['last_last_page_url']  = ""

        if report.last_prev_page > 0:
            self.request.session['last_prev_page_url']  = reverse('show_report_group_rule_page', args=[report.slug, view, group.slug, rule, report.last_prev_page])
            self.request.session['last_first_page_url'] = reverse('show_report_group_rule_page', args=[report.slug, view, group.slug, rule, report.last_first_page])

        if report.last_next_page > 0:
            self.request.session['last_next_page_url'] = reverse('show_report_group_rule_page', args=[report.slug, view, group.slug, rule, report.last_next_page])
            self.request.session['last_last_page_url'] = reverse('show_report_group_rule_page', args=[report.slug, view, group.slug, rule, report.last_last_page])

        report.update_last_page_urls(self.request.session)

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

class ReportAllPagesView(TemplateView):
    template_name = 'reports/report_all_pages.html'

    def get_context_data(self, **kwargs):
        context = super(ReportAllPagesView, self).get_context_data(**kwargs)

        view = kwargs['view']

        report = WebsiteReport.objects.get(slug=kwargs['report'])
        page = False
        groups = []

        if report.page_count == 1:
          page = report.get_first_page()
          if view == 'gl':
            groups = page.page_gl_results.all()
          elif view == 'rs':  
            groups = page.page_rs_results.all()
          else:  
            groups = page.page_rc_results.all()
            view = 'rc'

        self.request.session['last_report_slug'] = report.slug
        self.request.session['last_report_view'] = view
        self.request.session['last_report_page_count'] = report.page_count

        context['page']     = page
        context['report']   = report
        context['view']     = view
        context['summary']  = report
        context['groups']   = groups
        
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

        report.update_last_page_numbers(page.page_number)

        self.request.session['last_report_slug'] = report.slug
        self.request.session['last_report_view'] = view
        self.request.session['last_report_page_count'] = report.page_count

        self.request.session['last_page_number']   = report.last_page
        self.request.session['last_prev_page_url'] = ""
        self.request.session['last_next_page_url'] = ""
        self.request.session['last_first_page_url'] = ""
        self.request.session['last_last_page_url']  = ""

        if report.last_prev_page > 0:
            self.request.session['last_prev_page_url'] = reverse('show_report_page', args=[report.slug, view, report.last_prev_page])
            self.request.session['last_first_page_url'] = reverse('show_report_page', args=[report.slug, view, report.last_first_page])

        if report.last_next_page > 0:
            self.request.session['last_next_page_url'] = reverse('show_report_page', args=[report.slug, view, report.last_next_page])
            self.request.session['last_last_page_url'] = reverse('show_report_page', args=[report.slug, view, report.last_last_page])

        report.update_last_page_urls(self.request.session)

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
        group_slug = kwargs['group']

        report = WebsiteReport.objects.get(slug=kwargs['report'])
        page   = report.page_all_results.get(page_number=kwargs['page'])
        if view == 'gl':
          group = page.page_gl_results.get(slug=group_slug)
        elif view == 'rs':  
          group = page.page_rs_results.get(slug=group_slug)
        else:  
          group = page.page_rc_results.get(slug=group_slug)
          view_opt = 'rc'


        self.request.session['last_report_slug'] = report.slug
        self.request.session['last_report_view'] = view
        self.request.session['last_report_page_count'] = report.page_count

        report.update_last_page_numbers(page.page_number)

        self.request.session['last_page_number']   = report.last_page
        self.request.session['last_prev_page_url'] = ""
        self.request.session['last_next_page_url'] = ""
        self.request.session['last_first_page_url'] = ""
        self.request.session['last_last_page_url']  = ""

        if report.last_prev_page > 0:
            self.request.session['last_prev_page_url'] = reverse('show_report_page_group', args=[report.slug, view, report.last_prev_page, group_slug])
            self.request.session['last_first_page_url'] = reverse('show_report_page_group', args=[report.slug, view, report.last_first_page, group_slug])

        if report.last_next_page > 0:
            self.request.session['last_next_page_url'] = reverse('show_report_page_group', args=[report.slug, view, report.last_next_page, group_slug])
            self.request.session['last_last_page_url'] = reverse('show_report_page_group', args=[report.slug, view, report.last_last_page, group_slug])

        report.update_last_page_urls(self.request.session)


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
        group_slug = kwargs['group']
        rule_slug  = kwargs['rule']

        report = WebsiteReport.objects.get(slug=kwargs['report'])
        page   = report.page_all_results.get(page_number=kwargs['page'])
        if view == 'gl':
          group = page.page_gl_results.get(slug=group_slug)
        elif view == 'rs':  
          group = page.page_rs_results.get(slug=group_slug)
        else:  
          group = page.page_rc_results.get(slug=group_slug)
          view_opt = 'rc'

        page_rule_result = group.page_rule_results.get(slug=rule_slug)

        self.request.session['last_report_slug'] = report.slug
        self.request.session['last_report_view'] = view
        self.request.session['last_report_page_count'] = report.page_count

        report.update_last_page_numbers(page.page_number)

        self.request.session['last_page_number']   = report.last_page
        self.request.session['last_prev_page_url']  = ""
        self.request.session['last_next_page_url']  = ""
        self.request.session['last_first_page_url'] = ""
        self.request.session['last_last_page_url']  = ""

        if report.last_prev_page > 0:
            self.request.session['last_prev_page_url'] = reverse('show_report_page_group_rule', args=[report.slug, view, report.last_prev_page, group_slug, rule_slug])
            self.request.session['last_first_page_url'] = reverse('show_report_page_group_rule', args=[report.slug, view, report.last_first_page, group_slug, rule_slug])

        if report.last_next_page > 0:
            self.request.session['last_next_page_url'] = reverse('show_report_page_group_rule', args=[report.slug, view, report.last_next_page, group_slug, rule_slug])
            self.request.session['last_last_page_url'] = reverse('show_report_page_group_rule', args=[report.slug, view, report.last_last_page, group_slug, rule_slug])

        report.update_last_page_urls(self.request.session)        

        context['report']        = report
        context['view']          = view
        context['summary']       = page
        context['group']         = group
        context['page']          = page
        context['page_rule_result'] = page_rule_result
        context['result_messages']   = page_rule_result.result_message.split(';')        

        
        return context             


class URLInformationView(TemplateView):
    template_name = 'reports/url_information.html'

    def get_context_data(self, **kwargs):
        context = super(URLInformationView, self).get_context_data(**kwargs)

        report = WebsiteReport.objects.get(slug=kwargs['report'])

        context['report'] = report
        
        return context            
