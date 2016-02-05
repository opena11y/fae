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

DEBUG=False
INFO=True

def debug(s):
  if DEBUG:
    print("[ARCHIVED REPORTS][DEBUG]: " + s)

def info(s):
  if INFO:
    print("[ARCHIVED REPORTS][INFO]: " + s)

def error(s):
  print("[ARCHIVED REPORTS][**ERROR**]: " + s)


def main():

  message_flag = True

  while True:
    ws_eval_results = []
    
    now         = timezone.now();
    error_date  = now - timedelta(days=1)
    delete_date = now - timedelta(days=2)

    info("=================================================")
    info("          Now: " + str(now))
    info("   Error date: " + str(error_date ))
    info("  Delete date: " + str(delete_date))
    info("=================================================")
  
    for user in User.objects.all():
    
      if user.username == 'anonymous':
        continue
      else:

        # Delete any reports that had errors
        try:
          ws_reports = WebsiteReport.objects.filter(user=user, created__lt=error_date, status='E')

          if len(ws_reports):
            for wsr in ws_reports:
              try:
                wsr.delete()
              except:
                error("Error deleted: " + str(wsr))  
        except:
          error("Error accessing the database for status='E'")  

        # Delete the oldest reports over the saved limit
        try:
          ws_reports = WebsiteReport.objects.filter(user=user, created__lt=delete_date, status='C').exclude(archive=True).order_by('-created')
        except:
          error("Error accessing the database for status='E' and archived=True ")  
          
        profile = False  
        try:   
          profile = user.profile 
        except:  
          error("Error accessing profile: " + str(user))  

        if profile:

          max = profile.max_saved
          num = len(ws_reports)
          diff = num-max

          info("  User " + str(user) + "  " + str(num) + " unsaved reports old enough for deletion (Buffer " + str(max) + " reports)")

          if diff:
          
            i = 0;
            for wsr in ws_reports:
              if i < diff:
                try:  
                  wsr.set_status_summary()
                except:
                  error("Error setting website report to summary: " + str(wsr))
              i = i + 1    

    if DEBUG: 
      time.sleep(20) # wait 20 seconds between checks if in DEBUG mode
    else:           
      time.sleep(43200) # wait 12 hours between checks
          
if __name__ == "__main__":
  main()
