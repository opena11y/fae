from django.contrib import admin
from rules.models import Rule 
from rules.models import RuleScope 
from rules.models import RuleGroup 
from rules.models import InformationalLink, NodeResultMessage

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

class InformationalLinkAdmin(admin.ModelAdmin):
    list_display = ('rule', 'title', 'type', 'url')
    list_filter = ('rule', 'type')

admin.site.register(InformationalLink, InformationalLinkAdmin)


