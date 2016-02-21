from django.contrib import admin

# Register your models here.
from .models import WebsiteRuleResultGroup
from .models import WebsiteRuleCategoryResultGroup
from .models import WebsiteGuidelineResultGroup
from .models import WebsiteRuleScopeResultGroup
from .models import WebsiteReportGroup

class WebsiteReportGroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'num_total_reports', 'num_total_pages', 'implementation_pass_fail_score', 'implementation_score')

admin.site.register(WebsiteReportGroup, WebsiteReportGroupAdmin)


class WebsiteRuleCategoryResultGroupAdmin(admin.ModelAdmin):
    list_display = ('rule_category', 'wsr_group', 'implementation_pass_fail_score', 'implementation_score')
    list_filter  = ('wsr_group', 'rule_category')    

admin.site.register(WebsiteRuleCategoryResultGroup, WebsiteRuleCategoryResultGroupAdmin)

class WebsiteGuidelineResultGroupAdmin(admin.ModelAdmin):
    list_display = ('guideline', 'wsr_group',  'implementation_pass_fail_score', 'implementation_score')
    list_filter  = ('wsr_group', 'guideline')    

admin.site.register(WebsiteGuidelineResultGroup, WebsiteGuidelineResultGroupAdmin)

class WebsiteRuleScopeResultGroupAdmin(admin.ModelAdmin):
    list_display = ('rule_scope', 'wsr_group', 'implementation_pass_fail_score', 'implementation_score')
    list_filter  = ('wsr_group', 'rule_scope')    

admin.site.register(WebsiteRuleScopeResultGroup, WebsiteRuleScopeResultGroupAdmin)

class WebsiteRuleResultGroupAdmin(admin.ModelAdmin):
    list_display = ('rule', 'wsr_group', 'result_value',  'implementation_pass_fail_score', 'implementation_score')
    list_filter  = ('wsr_group', 'rule')    

admin.site.register(WebsiteRuleResultGroup, WebsiteRuleResultGroupAdmin)
