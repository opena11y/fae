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

file: fae-util/process_subscriptions.py

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

from django.db       import models
from reports.models  import WebsiteReport
from django.contrib.auth.models import User

from django.core.exceptions     import ObjectDoesNotExist

from userProfiles.models import UserProfile


DEBUG=True
INFO=True
ERROR=True

log = open(os.path.join(APP_DIR + 'logs/subscriptions-reports.log'), 'w')

def debug(s):
  if DEBUG and log:
    log.write("[SUBSCRIPTIONS][debug]: " + str(s) + "\n")
    log.flush()  
    print("[SUBSCRIPTIONS][debug]: " + str(s) + "\n")


def info(s):
  if INFO and log:
    log.write("[SUBSCRIPTIONS][info]: " + str(s) + "\n")
    log.flush()
    if DEBUG:
      print("[SUBSCRIPTIONS][info]: " + str(s) + "\n")

def error(s):
  if ERROR and log:
    log.write("[SUBSCRIPTIONS][**ERROR]: " + str(s) + "\n")
    log.flush()
    if DEBUG:
      print("[SUBSCRIPTIONS][**ERROR]: " + str(s) + "\n")


def update_subscriptions():

  info('Updating subscriptions: ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") )

  # Get all users
  user_profiles = UserProfile.objects.all()

  for up in user_profiles:

    up.update_subscription_status()
    up.check_for_email_subscription_notifications()

    if up.subscription_status == 'EXPIRED':
      if up.subscription_days == -1:
        info(str(up) + ": Expired 1 day ago")
      else:  
        info(str(up) + ": Expired " + str(abs(up.subscription_days)) + " days ago")
    else:
      if up.subscription_status == 'CURRENT':
        if up.subscription_days == 1:
          info(str(up) + ": Current, 1 day left")
        else:  
          info(str(up) + ": Current, " + str(up.subscription_days) + " days left")
      else:
        info(str(up) + ": Free")



if __name__ == "__main__":
  update_subscriptions()
