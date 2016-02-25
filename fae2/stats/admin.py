"""
Copyright 2014-2016 University of Illinois

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

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