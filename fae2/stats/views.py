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

        year             = StatsYear.objects.get(year=td.year)
        month            = StatsMonth.objects.get(stats_year=year, month=td.month)
        today            = StatsDay.objects.get(stats_month=month, date=td)


        context['year']   = year 
        context['month']  = month
        context['today']  = today
        
        return context            

