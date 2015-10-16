from django.contrib import admin

from manualChecks.models import  ManualCheck

class ManualCheckAdmin(admin.ModelAdmin):
    list_display = ('rule', 'title')
    list_filter  = ('rule',)

admin.site.register(ManualCheck, ManualCheckAdmin)


