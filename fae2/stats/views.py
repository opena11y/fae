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

