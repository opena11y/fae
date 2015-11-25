from django.contrib import admin

from .models import WebsiteReport
from .models import ProcessedURL
from .models import UnprocessedURL
from .models import FilteredURL


class WebsiteReportAdmin(admin.ModelAdmin):
    list_display = ('url', 'user', 'title', 'status', 'slug', 'ruleset', 'depth', 'created', 'last_viewed', 'data_directory')
    list_filter  = ('url', 'user')

admin.site.register(WebsiteReport, WebsiteReportAdmin)

class ProcessedURLAdmin(admin.ModelAdmin):
    list_display = ('page_seq_num', 'url_requested', 'url_returned')
    list_filter  = ('ws_report',)

admin.site.register(ProcessedURL, ProcessedURLAdmin)

class UnprocessedURLAdmin(admin.ModelAdmin):
    list_display = ('url', 'url_referenced')
    list_filter  = ('ws_report',)

admin.site.register(UnprocessedURL, UnprocessedURLAdmin)

class FilteredURLAdmin(admin.ModelAdmin):
    list_display = ('url', 'url_referenced')
    list_filter  = ('ws_report',)

admin.site.register(FilteredURL, FilteredURLAdmin)
