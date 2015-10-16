from django.contrib import admin

from .models import Ruleset

class RulesetAdmin(admin.ModelAdmin):
    list_display = ('title', 'tooltip', 'version', 'author')
    list_filter  = ('author', 'version')

admin.site.register(Ruleset, RulesetAdmin)

