"""
Copyright 2014-2018 University of Illinois

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

file: populate/user_info.py

Author: Jon Gunderson

"""

from __future__ import print_function
from __future__ import absolute_import
import sys
import os
import django
from django.core.exceptions import ObjectDoesNotExist
import datetime
import pytz

fp = os.path.realpath(__file__)
path, filename = os.path.split(fp)

fae2_path = path.split('/populate')[0]
sys.path.append(fae2_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fae2.settings')
from django.conf import settings

django.setup()

"""This file is for populating the database with markup information
I empty it. Run as a standalone script!"""

from django.core.exceptions      import ObjectDoesNotExist
from django.core.exceptions      import ImproperlyConfigured
from django.contrib.sites.models import Site
from django.contrib.auth.models  import User
from accounts.models             import AccountType
from userProfiles.models         import UserProfile
from websiteResultGroups.models  import WebsiteReportGroup
from stats.models                import StatsUser
from stats.models                import StatsRegisteredUsers
from reports.models              import WebsiteReport


def user_information(date, label):
  users_no_reports = 0
  users_one_report = 0
  users_more_than_one_report = 0
  users_more_than_five_reports = 0
  users_more_than_ten_reports = 0

  for u in User.objects.all():
    count = WebsiteReport.objects.filter(user=u).filter(created__gte=date).count()

    if count == 0:
      users_no_reports += 1

    if count == 1:
      users_one_report += 1

    if count > 1:
      users_more_than_one_report += 1

    if count > 5:
      users_more_than_five_reports += 1

    if count > 10:
      users_more_than_ten_reports += 1

  print('\n' + label)
  print('Users with no report: ' + str(users_no_reports))
  print('Users with one report: ' + str(users_one_report))
  print('Users with more than one report: ' + str(users_more_than_one_report))


users_total = 0
print('Total Users: ' + str(User.objects.all().count()))

user_information(datetime.datetime(2019, 7, 1, tzinfo=pytz.UTC), 'Last 6 months')
user_information(datetime.datetime(2019, 1, 1, tzinfo=pytz.UTC), 'Last 12 months')
user_information(datetime.datetime(2018, 7, 1, tzinfo=pytz.UTC), 'Last 18 months')
user_information(datetime.datetime(2018, 1, 1, tzinfo=pytz.UTC), 'Last 24 months')
user_information(datetime.datetime(2013, 1, 1, tzinfo=pytz.UTC), 'All time')

