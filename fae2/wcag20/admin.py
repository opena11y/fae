from django.contrib import admin

from wcag20.models import WCAG20_Principle, WCAG20_Guideline, WCAG20_SuccessCriterion

class WCAG20_PrincipleAdmin(admin.ModelAdmin):
    list_display = ('title', 'num', 'url')

admin.site.register(WCAG20_Principle, WCAG20_PrincipleAdmin)

class WCAG20_GuidelineAdmin(admin.ModelAdmin):
    list_display = ('title', 'num', 'url')

admin.site.register(WCAG20_Guideline, WCAG20_GuidelineAdmin)

class WCAG20_SuccessCriterionAdmin(admin.ModelAdmin):
    list_display = ('title', 'num', 'level', 'url')
    list_filter  = ('level', )

admin.site.register(WCAG20_SuccessCriterion, WCAG20_SuccessCriterionAdmin)


