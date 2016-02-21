from django.contrib import admin

# Register your models here.

from .models import StatsYear
from .models import StatsMonth
from .models import StatsDay
from .models import StatsUser

class StatsYearAdmin(admin.ModelAdmin):
    list_display = ('year', )

admin.site.register(StatsYear, StatsYearAdmin)

class StatsMonthAdmin(admin.ModelAdmin):
    list_display = ('month', 'stats_year')

admin.site.register(StatsMonth, StatsMonthAdmin)

class StatsDayAdmin(admin.ModelAdmin):
    list_display = ('date', 'stats_month')

admin.site.register(StatsDay, StatsDayAdmin)

class StatsUserAdmin(admin.ModelAdmin):
    list_display = ('user', )

admin.site.register(StatsUser, StatsUserAdmin)