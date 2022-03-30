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

from datetime import datetime, timedelta
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

any_saved_reports_count = 0
current_user_count  = 0
deleted_user_count  = 0
subscriber_count = 0
recent_count = 0


for su in stats_users:

    flag = False

    count = WebsiteReport.objects.filter(user=su.user).count()
    if count > 1:
      any_saved_reports_count += 1
      flag = True

    if su.user.profile.account_type.type_id > 1:
      subscriber_count += 1
      flag = True

    if su.user.date_joined > datetime.today():
      recent_count += 1
      flag = True

    if flag:
      current_user_count += 1
    else:
      deleted_user_count += 1

print('    Any Saved: ' + str(any_saved_reports_count))
print('  Subscribers: ' + str(subscriber_count))
print('       Recent: ' + str(recent_count))
print('Current Users: ' + str(current_user_count))
print('Deleted Users: ' + str(deleted_user_count))


