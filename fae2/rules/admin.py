from django.contrib import admin
from .models import Rule 
from .models import RuleScope 
from .models import RuleGroup 
from .models import RuleMapping
from .models import RuleCategoryRuleMapping 
from .models import GuidelineRuleMapping 
from .models import SuccessCriterionRuleMapping 
from .models import NodeResultMessage

class RuleAdmin(admin.ModelAdmin):
    list_display = ('nls_rule_id', 'summary', 'wcag_primary', 'category', 'scope', 'group')
    list_filter = ('wcag_primary', 'category', 'scope', 'group')
    exclude = ('purpose_1_html', 'purpose_2_html', 'purpose_3_html', 'purpose_4_html', 'definition_html', 'summary_html', 'target_resource_desc_html')
    
admin.site.register(Rule, RuleAdmin)

class RuleScopeAdmin(admin.ModelAdmin):
    list_display = ('title', 'abbrev', 'rule_scope_code')
    
admin.site.register(RuleScope, RuleScopeAdmin)

class RuleGroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'rule_group_code')
    
admin.site.register(RuleGroup, RuleGroupAdmin)

class NodeResultMessageAdmin(admin.ModelAdmin):
    list_display = ('label', 'rule', 'message', 'updated_date')
    list_filter = ('rule',)

admin.site.register(NodeResultMessage, NodeResultMessageAdmin)

class RuleMappingAdmin(admin.ModelAdmin):
    list_display = ('ruleset', 'rule', 'required', 'enabled')
    list_filter  = ('ruleset', 'rule', 'required', 'enabled')

admin.site.register(RuleMapping, RuleMappingAdmin)

class RuleCategoryRuleMappingAdmin(admin.ModelAdmin):
    list_display = ('ruleset', 'rule_category')
    list_filter  = ('ruleset', 'rule_category')

admin.site.register(RuleCategoryRuleMapping, RuleCategoryRuleMappingAdmin)

class GuidelineRuleMappingAdmin(admin.ModelAdmin):
    list_display = ('ruleset', 'guideline')
    list_filter  = ('ruleset', 'guideline')

admin.site.register(GuidelineRuleMapping, GuidelineRuleMappingAdmin)

class SuccessCriterionRuleMappingAdmin(admin.ModelAdmin):
    list_display = ('guideline_rule_mapping', 'success_criterion')
    list_filter  = ('guideline_rule_mapping__ruleset', 'success_criterion')

admin.site.register(SuccessCriterionRuleMapping, SuccessCriterionRuleMappingAdmin)

