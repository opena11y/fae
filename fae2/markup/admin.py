from django.contrib import admin
from markup.models import ElementDefinition, LanguageSpec


class ElementDefinitionAdmin(admin.ModelAdmin):
    list_display = ('spec', 'element','attribute','value', 'description', 'url' )
    list_filter = ( 'spec','element', 'attribute')

admin.site.register(ElementDefinition, ElementDefinitionAdmin)

class LanguageSpecAdmin(admin.ModelAdmin):
    list_display = ('abbr', 'title', 'url' )

admin.site.register(LanguageSpec, LanguageSpecAdmin)

