from django.contrib import admin

from reports.models import WebsiteEvaluationReport

class WebsiteEvaluationReportAdmin(admin.ModelAdmin):
    list_display = ('url', 'user', 'title', 'slug', 'implementation_score', 'implementation_status', 'ruleset', 'depth', 'rules_violation', 'rules_warning', 'rules_manual_check', 'rules_passed', 'created', 'last_viewed', 'data_directory')
    list_filter  = ('url', 'user')

admin.site.register(WebsiteEvaluationReport, WebsiteEvaluationReportAdmin)