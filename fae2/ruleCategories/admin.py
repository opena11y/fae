from django.contrib import admin

from ruleCategories.models import  RuleCategory

class RuleCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'rule_category_code', 'category_id', 'slug')

admin.site.register(RuleCategory, RuleCategoryAdmin)

