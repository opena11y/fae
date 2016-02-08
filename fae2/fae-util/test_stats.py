import sys
import os
import string
import glob

import optparse
import subprocess
import shlex
import time
import getopt
import shutil
import json
import csv
import re
import datetime

from os.path import join, getsize

import urllib

sys.path.append(os.path.abspath('..'))

from django.utils.encoding  import iri_to_uri

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fae2.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.conf import settings

from django.core.exceptions import ObjectDoesNotExist


from stats.models  import StatsYear
from stats.models  import StatsMonth
from stats.models  import StatsDay

from websiteResultGroups.models  import WebsiteReportGroup

DEBUG=True
INFO=True
ERROR=True

def debug(s):
  if DEBUG:
    print ("[TEST STATS][debug  ]: " + str(s))

def info(s):
  if INFO:
    print ("[TEST STATS][info   ]: " + str(s))

def error(s):
  if ERROR:
    print ("[TEST STATS][**ERROR]: " + str(s))

today = datetime.date.today()
info(str(today))
try:
  year = StatsYear.objects.get(year=today.year)
  debug("[YEAR] exists")
except:
  wsrg =  WebsiteReportGroup(title="Summary of results year: " + str(today.year))
  wsrg.save()
  year = StatsYear(year=today.year, ws_report_group=wsrg) 
  year.save()  
  debug("[YEAR] created")

try:
  month = StatsMonth.objects.get(stats_year=year, month=today.month)
  debug("[MONTH] exits")
except:
  wsrg =  WebsiteReportGroup(title="Summary of results month: " + str(today.year) + "-" + str(today.month))
  wsrg.save()
  month = StatsMonth(stats_year=year, month=today.month, ws_report_group=wsrg)  
  month.save()
  debug("[MONTH] created")

try:
  day = StatsDay.objects.get(stats_month=today.month, date=today)
  debug("[DAY] exists")
except:
  wsrg =  WebsiteReportGroup(title="Summary of results day: " + str(today.year) + "-" + str(today.month) + "-" + str(today.day))
  wsrg.save()
  day = StatsDay(stats_month=month, date=today, ws_report_group=wsrg)  
  day.save()
  debug("[DAY] created")



