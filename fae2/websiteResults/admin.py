from django.contrib import admin


from .models import WebsiteRuleCategoryResult
from .models import WebsiteGuidelineResult
from .models import WebsiteRuleScopeResult
from .models import WebsiteRuleResult


class WebsiteRuleCategoryResultAdmin(admin.ModelAdmin):
    list_display = ('rule_category', 'slug', 'ws_report', 'rules_violation', 'rules_warning', 'rules_manual_check', 'rules_passed', 'implementation_pass_fail_score', 'implementation_score', 'implementation_status')
    list_filter  = ('ws_report', 'rule_category')    

admin.site.register(WebsiteRuleCategoryResult, WebsiteRuleCategoryResultAdmin)

class WebsiteGuidelineResultAdmin(admin.ModelAdmin):
    list_display = ('guideline', 'slug', 'ws_report', 'rules_violation', 'rules_warning', 'rules_manual_check', 'rules_passed', 'implementation_pass_fail_score', 'implementation_score', 'implementation_status')
    list_filter  = ('ws_report', 'guideline')    

admin.site.register(WebsiteGuidelineResult, WebsiteGuidelineResultAdmin)

class WebsiteRuleScopeResultAdmin(admin.ModelAdmin):
    list_display = ('rule_scope', 'slug', 'ws_report', 'rules_violation', 'rules_warning', 'rules_manual_check', 'rules_passed', 'implementation_pass_fail_score', 'implementation_score', 'implementation_status')
    list_filter  = ('ws_report', 'rule_scope')    

admin.site.register(WebsiteRuleScopeResult, WebsiteRuleScopeResultAdmin)

class WebsiteRuleResultAdmin(admin.ModelAdmin):
    list_display = ('rule', 'ws_report', 'result_value', 'pages_violation', 'pages_warning', 'pages_manual_check', 'pages_passed', 'pages_na', 'implementation_pass_fail_score', 'implementation_score', 'implementation_status')
    list_filter  = ('ws_report', 'rule')    

admin.site.register(WebsiteRuleResult, WebsiteRuleResultAdmin)

