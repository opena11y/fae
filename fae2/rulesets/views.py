from django.http import HttpResponse
from django.views.generic import TemplateView
from ruleCategories.models import RuleCategory
from wcag20.models import WCAG20_Guideline
from .models import Ruleset

class RulesetsView(TemplateView):
    template_name = 'rulesets/rulesets_view.html'

    def get_context_data(self, **kwargs):
        context = super(RulesetsView, self).get_context_data(**kwargs)

        context['rule_categories'] = RuleCategory.objects.all()
        context['rulesets']        = Ruleset.objects.all()
        
        return context

class RulesetsWCAGView(TemplateView):
    template_name = 'rulesets/rulesets_wcag_view.html'

    def get_context_data(self, **kwargs):

        context = super(RulesetsWCAGView, self).get_context_data(**kwargs)

        context['guidelines'] = WCAG20_Guideline.objects.all()
        context['rulesets']   = Ruleset.objects.all()
        
        return context

class RulesetsRuleView(TemplateView):
    template_name = 'rulesets/rulesets_rule_view.html'

    def get_context_data(self, **kwargs):
        context = super(RulesetsRuleView, self).get_context_data(**kwargs)

        context['rulesets']   = Ruleset.objects.all()
        context['rule']       = Rule.objects.get(slug=kwargs['rule_num'])

        return context

class RulesetsRuleWCAGView(TemplateView):
    template_name = 'rulesets/rulesets_rule_wcag_view.html'

    def get_context_data(self, **kwargs):
        context = super(RulesetsRuleWCAGView, self).get_context_data(**kwargs)

        context['rulesets']   = Ruleset.objects.all()
        context['rule']       = Ruleset.objects.get(slug=kwargs['rule_num'])
        return context

class RulesetView(TemplateView):
    template_name = 'rulesets/ruleset_view.html'

    def get_context_data(self, **kwargs):
        context = super(RulesetView, self).get_context_data(**kwargs)

        context['ruleset'] = Ruleset.objects.get(slug=kwargs['slug'])
        return context


class RulesetWCAGView(TemplateView):
    template_name = 'rulesets/ruleset_wcag_view.html'

    def get_context_data(self, **kwargs):
        context = super(RulesetWCAGView, self).get_context_data(**kwargs)

        context['ruleset'] = Ruleset.objects.get(slug=kwargs['slug'])
        return context

class RulesetRuleView(TemplateView):
    template_name = 'rulesets/rulesets_rule_view.html'

    def get_context_data(self, **kwargs):
        context = super(RulesetRuleView, self).get_context_data(**kwargs)

        context['ruleset']         = Ruleset.objects.get(slug=kwargs['slug'])
        context['rule']            = Rule.objects.get(slug=kwargs['rule_num'])
        return context

class RulesetRuleWCAGView(TemplateView):
    template_name = 'rulesets/ruleset_rule__wcag_view.html'

    def get_context_data(self, **kwargs):
        context = super(RulesetRuleWCAGView, self).get_context_data(**kwargs)

        context['ruleset'] = Ruleset.objects.get(slug=kwargs['slug'])
        context['rule']    = Rule.objects.get(slug=kwargs['rule_num'])
        return context


