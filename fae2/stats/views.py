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

from django.shortcuts import render

from django.http import HttpResponse 
from django.http import JsonResponse
from django.shortcuts import redirect

import datetime

from django.views.generic import TemplateView

from django.contrib.auth.models import User

from .models import StatsYear
from .models import StatsMonth
from .models import StatsDay
from .models import StatsUser

# Create your views here.

class ShowUsageStatistics(TemplateView):
    template_name = 'stats/summary.html'

    def get_context_data(self, **kwargs):
        context = super(ShowUsageStatistics, self).get_context_data(**kwargs)

        td= datetime.date.today()

        year   = StatsYear.objects.get(year=td.year)
        years  = StatsYear.objects.all()

        month  = StatsMonth.objects.get(stats_year=year, month=td.month)
        months = StatsMonth.objects.all()

        today  = StatsDay.objects.get(stats_month=month, date=td)
        days   = StatsDay.objects.all()[:7]

        anonymous       = User.objects.get(username="anonymous")
        user_stats      = StatsUser.objects.exclude(user=anonymous)
        anonymous_stats = StatsUser.objects.get(user=anonymous)         

        context['year']   = year 
        context['month']  = month
        context['today']  = today

        context['user_stats'] = user_stats
        context['anonymous_stats'] = anonymous_stats
        
        return context            

