from django.contrib import admin


from .models import WebsiteResult
from .models import WebsiteRuleCategoryResult
from .models import WebsiteGuidelineResult
from .models import WebsiteRuleScopeResult
from .models import WebsiteRuleResult

class WebsiteResultAdmin(admin.ModelAdmin):
    list_display = ('ws_report', 'rules_violation', 'rules_warning', 'rules_manual_check', 'rules_passed', 'implementation_score', 'implementation_status')

admin.site.register(WebsiteResult, WebsiteResultAdmin)


class WebsiteRuleCategoryResultAdmin(admin.ModelAdmin):
    list_display = ('rule_category', 'ws_report', 'rules_violation', 'rules_warning', 'rules_manual_check', 'rules_passed', 'implementation_score', 'implementation_status')
    list_filter  = ('ws_report', 'rule_category')    

admin.site.register(WebsiteRuleCategoryResult, WebsiteRuleCategoryResultAdmin)

class WebsiteGuidelineResultAdmin(admin.ModelAdmin):
    list_display = ('guideline', 'ws_report', 'rules_violation', 'rules_warning', 'rules_manual_check', 'rules_passed', 'implementation_score', 'implementation_status')
    list_filter  = ('ws_report', 'guideline')    

admin.site.register(WebsiteGuidelineResult, WebsiteGuidelineResultAdmin)

class WebsiteRuleScopeResultAdmin(admin.ModelAdmin):
    list_display = ('rule_scope', 'ws_report', 'rules_violation', 'rules_warning', 'rules_manual_check', 'rules_passed', 'implementation_score', 'implementation_status')
    list_filter  = ('ws_report', 'rule_scope')    

admin.site.register(WebsiteRuleScopeResult, WebsiteRuleScopeResultAdmin)

class WebsiteRuleResultAdmin(admin.ModelAdmin):
    list_display = ('rule', 'ws_result', 'pages_violation', 'pages_warning', 'pages_manual_check', 'pages_passed', 'pages_na', 'implementation_score', 'implementation_status')
    list_filter  = ('ws_result', 'rule')    

admin.site.register(WebsiteRuleResult, WebsiteRuleResultAdmin)

