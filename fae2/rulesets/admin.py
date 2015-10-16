from django.contrib import admin

from rulesets.models import Ruleset, RuleMapping

class RulesetAdmin(admin.ModelAdmin):
    list_display = ('title', 'tooltip', 'version', 'author')
    list_filter  = ('author', 'version')

admin.site.register(Ruleset, RulesetAdmin)

class RuleMappingAdmin(admin.ModelAdmin):
    list_display = ('ruleset', 'rule', 'required', 'enabled')
    list_filter  = ('ruleset', 'rule', 'required', 'enabled')

admin.site.register(RuleMapping, RuleMappingAdmin)
