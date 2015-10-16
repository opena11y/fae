from django.http import HttpResponse
from django.views.generic import TemplateView
from ruleCategories.models import RuleCategory
from .models import Ruleset

class RulesetsView(TemplateView):
    template_name = 'rulesets/rulesets_view.html'

    def get_context_data(self, **kwargs):
        rule_categories = RuleCategory.objects.all()
        rulesets  = Ruleset.objects.all()

        context = super(RulesetsView, self).get_context_data(**kwargs)

        context['rule_groupings'] = rule_categories
        context['rulesets']       = rulesets
        
        return context

class RulesetView(TemplateView):
    template_name = 'rulesets/ruleset_view.html'

    def get_context_data(self, **kwargs):
        context = super(RulesetView, self).get_context_data(**kwargs)
        context['ruleset'] = Ruleset.objects.get(slug=kwargs['slug'])
        return context
