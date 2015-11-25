from django.contrib import admin

from wcag20.models import Principle, Guideline, SuccessCriterion

class PrincipleAdmin(admin.ModelAdmin):
    list_display = ('title', 'num', 'url')

admin.site.register(Principle, PrincipleAdmin)

class GuidelineAdmin(admin.ModelAdmin):
    list_display = ('title', 'num', 'url')

admin.site.register(Guideline, GuidelineAdmin)

class SuccessCriterionAdmin(admin.ModelAdmin):
    list_display = ('title', 'num', 'level', 'url')
    list_filter  = ('level', )

admin.site.register(SuccessCriterion, SuccessCriterionAdmin)


