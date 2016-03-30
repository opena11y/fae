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
from fae2.settings import PROCESSING_THREADS

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


def archive_reports():

  info('Processing archived reports: ' + datetime.now().strftime("%Y-%m-%d %H:%M") )

  # Delete reports with errors
  error_reports = WebsiteReport.objects.filter(status='E')

  for r in error_reports:
    try:
      info("  Deleting:" + r.title)
      r.delete()
    except:
      error("Error deleting (error): " + str(r))  

  # Delete reports with marked for deletion
  reports_marked_for_deletion = WebsiteReport.objects.filter(status='D')

  for r in reports_marked_for_deletion:
    try:
      info("  Summary (marked):" + r.title)
      r.set_status_summary()
    except:
      error("Error summary (marked): " + str(r))  

  for user_profile in UserProfile.objects.all():
    
    if user_profile.user.username == 'anonymous':
      continue
    else:
      [reports, other_reports] = user_profile.get_active_reports()

    for r in other_reports:
      try:
        info("  Summary (other):" + r.title)
        r.set_status_summary()
      except:
        error("Error summary (other): " + str(r))          

if __name__ == "__main__":
  archive_reports()
