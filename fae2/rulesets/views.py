from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import Ruleset
from .models import compare_rulesets

class RulesetsView(TemplateView):
    template_name = 'rulesets/rulesets_view.html'

    def get_context_data(self, **kwargs):
        rulesets = Ruleset.objects.exclude(slug__contains="TEST")
        context = super(RulesetsView, self).get_context_data(**kwargs)
        context['rulesets'] = rulesets
        context['compare']  = compare_rulesets(rulesets, 'rc') 
        return context

class RulesetView(TemplateView):
    template_name = 'rulesets/ruleset_view.html'

    def get_context_data(self, **kwargs):
        context = super(RulesetView, self).get_context_data(**kwargs)
        context['ruleset'] = Ruleset.objects.get(slug=kwargs['slug'])
        return context
