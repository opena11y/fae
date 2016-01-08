from django.http import HttpResponse
from django.views.generic import TemplateView

class Disclaimer(TemplateView):
    template_name = 'abouts/disclaimer.html'

class ConceptsTerms(TemplateView):
    template_name = 'abouts/concepts_terms.html'

class Overview(TemplateView):
    template_name = 'abouts/overview.html'

class Privacy(TemplateView):
    template_name = 'abouts/privacy.html'

class ReportIssues(TemplateView):
    template_name = 'abouts/report_issues.html'

class Versions(TemplateView):
    template_name = 'abouts/versions.html'

