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

file: fae-util/user_account_reports.py

Author: Jon Gunderson

"""

from __future__ import print_function
from __future__ import absolute_import
import sys
import os
import string
import glob

import optparse
import shlex
import time
import getopt
import shutil
import datetime
import shutil

import django

fp = os.path.realpath(__file__)
path, filename = os.path.split(fp)
os.environ['FAE_HOME'] = path

fae_util_path = path

fae2_path = path.split('/fae-util')[0]

# print("[fae2_path]"+ str(fae2_path))

sys.path.append(fae2_path)

# print("PATH="+ str(sys.path))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fae2.settings')
django.setup()

from django.conf import settings

from fae2.settings import APP_DIR
from fae2.settings import PROCESSING_THREADS

from django.db       import models
from reports.models  import WebsiteReport
from django.contrib.auth.models import User

from django.core.exceptions     import ObjectDoesNotExist

from django.contrib.auth.models import User
from userProfiles.models import UserProfile
from userProfiles.models import InstitutionalProfile
from accounts.models import AccountType
from stats.models import StatsUser
from websiteResultGroups.models import WebsiteReportGroup

from reports.models import WebsiteReport

from datetime import datetime
from django.utils.timezone import make_aware
from django.utils import timezone
import pytz

DEBUG=True
INFO=True
ERROR=True

log = open(os.path.join(APP_DIR + 'logs/archived-reports.log'), 'w')

def debug(s):
  if DEBUG and log:
    log.write("[ARCHIVED REPORTS][debug]: " + str(s) + "\n")
    log.flush()
    print("[ARCHIVED REPORTS][debug]: " + str(s) + "\n")


def info(s):
  if INFO and log:
    log.write("[ARCHIVED REPORTS][info]: " + str(s) + "\n")
    log.flush()
    if DEBUG:
      print("[ARCHIVED REPORTS][info]: " + str(s) + "\n")

def error(s):
  if ERROR and log:
    log.write("[ARCHIVED REPORTS][**ERROR]: " + str(s) + "\n")
    log.flush()
    if DEBUG:
      print("[ARCHIVED REPORTS][**ERROR]: " + str(s) + "\n")


user_profiles = UserProfile.objects.all()

stats_users = StatsUser.objects.exclude(user__username="anonymous")

last_30_days  = 0
last_90_days  = 0
last_6_months = 0
last_year     = 0
any_saved_reports = 0

subscribers = 0
registered = 0

inactive = []

for su in stats_users:

    flag = False

    count = WebsiteReport.objects.filter(user=su.user).count()
    if count > 0:
      any_saved_reports += 1
      flag = True

    if su.reports_last_30_days > 0:
      last_30_days += 1
      flag = True

    if su.reports_last_90_days  > 0:
      last_90_days  += 1
      flag = True

    if su.reports_last_6_months > 0:
      last_6_months += 1
      flag = True

    if su.reports_last_year > 0:
      last_year += 1
      flag = True

    if su.user.profile.account_type.type_id > 1:
      subscribers += 1
      flag = True
    else:

      if not flag:
        inactive.append(su.user)

    registered += 1

print('         30 days: ' + str(last_30_days))
print('         90 days: ' + str(last_90_days))
print('        6 months: ' + str(last_6_months))
print('       last year: ' + str(last_year))
print('any saved report: ' + str(any_saved_reports))


print('   Inactive: ' + str(len(inactive)))
print('Subscribers: ' + str(subscribers))
print(' Registered: ' + str(registered))
