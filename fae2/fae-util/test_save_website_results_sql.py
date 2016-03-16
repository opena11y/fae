from __future__ import print_function
from __future__ import absolute_import
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
import django

sys.path.append(os.path.abspath('..'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fae2.settings')
django.setup()


from save_website_results_sql import saveResultsToDjango

from reports.models import WebsiteReport

    
def main():

  message_flag = True

  ws_reports = WebsiteReport.objects.all()
  
  if len(ws_reports):
    ws_report = ws_reports[0]

    # Removed any previous database relationships
    ws_report.processed_urls.all().delete()
    ws_report.unprocessed_urls.all().delete()
    ws_report.filtered_urls.all().delete()
    ws_report.filtered_urls.all().delete()

    ws_report.ws_gl_results.all().delete()
    ws_report.ws_rc_results.all().delete()
    ws_report.ws_rs_results.all().delete()

    ws_report.page_all_results.all().delete()

    print("=======================")
    print("Saving Data: " + str(ws_report))
    saveResultsToDjango(ws_report)

          
if __name__ == "__main__":
  main()
