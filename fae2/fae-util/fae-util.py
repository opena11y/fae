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
import urllib

import cmd

sys.path.append(os.path.abspath('..'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fae2.settings')
from django.conf import settings

from fae2.settings import APP_DIR

from django.db       import models
from reports.models  import WebsiteReport

# from save_website_results_sql import saveResultsToDjango

DEBUG=True
INFO=True

def debug(s):
  if DEBUG:
    print("[FAE-UTIL][DEBUG]: " + str(s))

def info(s):
  if INFO:
    print("[FAE-UTIL][INFO]: " + str(s))

def error(s):
  print("[FAE-UTIL][ERROR]: " + str(s))


def initWebsiteReport(ws_report):

  data_dir       = ws_report.data_directory 
  data_prop_file = ws_report.data_property_file
  data_auth_file = ws_report.data_authorization_file
  data_urls_file = ws_report.data_multiple_urls_file
  
  if os.path.exists(data_dir):
     shutil.rmtree(data_dir)
          
  os.makedirs(data_dir)
          
  file_prop = open(data_prop_file, 'w')

  if len(data_urls_file) > 0:  
    file_prop.write("multipleUrls=" + data_urls_file + "\n")
  else:    
    file_prop.write("url=" + ws_report.url + "\n")

#  if len(data_auth_file) > 0:  
#    file_prop.write("authorization=" +  data_auth_file + "\n")     
  
  file_prop.write("recommendedRules=true\n");
  
  file_prop.write("depth="   + str(ws_report.depth) + "\n")
  file_prop.write("ruleset=" + ws_report.ruleset.ruleset_id + "\n")
  file_prop.write("wait="    + str(ws_report.wait_time) + "\n")

  file_prop.write("spanDomains="    + ws_report.span_sub_domains    + "\n") 
  file_prop.write("excludeDomains=" + ws_report.exclude_sub_domains + "\n") 
  file_prop.write("includeDomains=" + ws_report.include_domains     + "\n")

  file_prop.write("outputDirectory=" + ws_report.data_directory     + "/data" + "\n")

  file_prop.write("browserVersion=" + ws_report.browser_emulation   + "\n")

  file_prop.write("scripts=openajax_a11y/scripts.txt\n")
  file_prop.write("exportFunction=toJSON\n")
  file_prop.write("exportExtension=json\n")
  file_prop.write("exportOption=true\n")

  file_prop.close()
  
  if len(data_auth_file) > 0:  
    file_auth = open(data_auth_file, 'w')
    file_auth.write('<?xml version="1.0" encoding="UTF-8"?>' + '\n')
    file_auth.write('<authorizations>' + '\n') 
    file_auth.write(ws_report.authorization.replace('\r', ''))    
    file_auth.write('</authorizations>' + '\n') 
    file_auth.close()

  if len(data_urls_file) > 0:  
    file_ws_urls = open(data_urls_file, 'w')
    for ws_url in ws_report.ws_eval_urls.all():
      if ws_url.valid:
        file_ws_urls.write(ws_url.url + "\n")    
      
    file_ws_urls.close()

  return

def analyzeWebsiteReport(ws_report):

  def countResultFiles(dir):
    fname = dir + "/processed_urls.csv"
    try:
      with open(fname) as f:
        return len(f.readlines())
      return 0      
    except:
      error("Error opening: " + fname)
      return 0    

  start = time.time()

  cmd = []
  cmd.append(settings.APP_DIR + 'fae2/fae-util/run')

  cmd.append('-c')
  cmd.append(ws_report.data_property_file)

  if len(ws_report.data_authorization_file):
    cmd.append('-a')
    cmd.append(ws_report.data_authorization_file)

  proc = subprocess.call(cmd)      
        
  page_count = countResultFiles(ws_report.data_directory + "/data")

  ave_time = "{:10.4f}".format(time.time()-start) + " seconds (0 pages)"
  if page_count > 0:
    if page_count == 1:
      ave_time = "{:10.4f}".format(time.time()-start) + " seconds/page (1 page)"
    else:  
      ave_time = "{:10.4f}".format((time.time()-start)/page_count) + " seconds/page (" + str(page_count) + " pages)"
  
  info("  Pages analyzed: " + str(page_count))
  info('Average processing time per page: ' + ave_time) 


def main():

  message_flag = True

  debug(APP_DIR)

  ws_reports = WebsiteReport.objects.filter(status="-")

  debug(len(ws_reports))
  
  if len(ws_reports):
    ws_report = ws_reports[0]

    info("=======================")
    info("Initializing report: " + str(ws_report))
    ws_report.set_status_initialized()
    initWebsiteReport(ws_report)

    info("Analyze website: " + str(ws_report))
    ws_report.set_status_analyzing()
    count = analyzeWebsiteReport(ws_report)

    info("Saving Data: " + str(ws_report))
    ws_report.set_status_saving()
#    saveResultsToDjango(ws_report)

          
if __name__ == "__main__":
  main()
