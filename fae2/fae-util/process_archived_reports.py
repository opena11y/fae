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
import fnmatch

import cmd
import django

from os.path import join 

from datetime import datetime, timedelta

from django.utils import timezone

sys.path.append(os.path.abspath('..'))

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


def delete_old_reports():

  # Delete reports with errors
  error_reports = WebsiteReport.objects.filter(status='E')

  for r in error_reports:
    try:
      r.delete()
    except:
      error("Error deleting at report with errors: " + str(r))  

  # Delete reports with marked for deletion
  reports_marked_to_delete = WebsiteReport.objects.filter(status='D')

  for r in reports_marked_to_delete:
    try:
      r.set_status_summary()
    except:
      error("Error deleting a report marked for deletion: " + str(r))  

  for user_profile in UserProfile.objects.all():
    
    if user_profile.user.username == 'anonymous':
      continue
    else:
      [reports, old_reports] = user_profile.get_active_reports()

    for r in old_reports:
      try:
        r.set_status_summary()
      except:
        error("Error deleting at old report: " + str(r))          

if __name__ == "__main__":
  delete_old_reports()
