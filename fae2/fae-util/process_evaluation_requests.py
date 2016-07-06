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

file: fae-util/process_evaluation_requests.py

Author: Jon Gunderson

"""

from __future__ import division
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
import urllib

import cmd
import django

import threading

fp = os.path.realpath(__file__)
path, filename = os.path.split(fp)
os.environ['FAE_HOME'] = path

fae_util_path = path

fae2_path = path.split('/fae-util')[0]
sys.path.append(fae2_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fae2.settings')
django.setup()

from django.conf import settings

from fae2.settings import APP_DIR
from fae2.settings import PROCESSING_THREADS

from django.db       import models
from reports.models  import WebsiteReport

from save_website_results_sql import saveResultsToDjango

DEBUG=True
INFO=True

log = open(os.path.join(APP_DIR + 'logs/process-evaluation.log'), 'w')

print(str(log))

def debug(s):
  if DEBUG and log:
    log.write('[PROC_EVAL_REQ][DEBUG]: ' + str(s) + '\n')
    log.flush()

def info(s):
  if INFO and log:
    try: 
      log.write('[PROC_EVAL_REQ][INFO]: ' + str(s) + '\n')
      log.flush()
      print('[PROC_EVAL_REQ][INFO]: ' + str(s))
    except:
      log.write('[PROC_EVAL_REQ][INFO]: error in string "s" \n')
      log.flush()
      print('[PROC_EVAL_REQ][INFO]: error in string "s" \n')
      

def error(s):
  if log:
    try:
      log.write('[PROC_EVAL_REQ][**ERROR]: ' + str(s) + '\n')
      log.flush()
    except:
      log.write('[PROC_EVAL_REQ][**ERROR]: error in string "s" \n')
      log.flush()
      

def init_oaa_script_file():
  f = open(fae_util_path + '/openajax_a11y/scripts.txt', 'w')
  f.write(fae_util_path + '/openajax_a11y/oaa_a11y_evaluation.js\n')
  f.write(fae_util_path + '/openajax_a11y/oaa_a11y_rules.js\n')
  f.write(fae_util_path + '/openajax_a11y/oaa_a11y_rulesets.js\n')
  f.close()


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
    file_prop.write("multipleUrls=" + data_urls_file + '\n')
  else:    
    file_prop.write("url=" + ws_report.url + '\n')

#  if len(data_auth_file) > 0:  
#    file_prop.write("authorization=" +  data_auth_file + '\n')     
  
  file_prop.write('recommendedRules=true\n');
  
  file_prop.write('depth='   + str(ws_report.depth) + '\n')
  file_prop.write('ruleset=' + ws_report.ruleset.ruleset_id + '\n')
  if ws_report.max_pages > 0:
    file_prop.write('maxPages=' + str(ws_report.max_pages) + '\n')

  file_prop.write('wait='    + str(ws_report.wait_time) + '\n')

  file_prop.write("spanDomains="    + ws_report.span_sub_domains    + '\n') 
  file_prop.write("excludeDomains=" + ws_report.exclude_sub_domains + '\n') 
  file_prop.write("includeDomains=" + ws_report.include_domains     + '\n')

  file_prop.write("outputDirectory=" + ws_report.data_directory + '/data' + '\n')

  file_prop.write("browserVersion=" + ws_report.browser_emulation   + '\n')

  file_prop.write("scripts=" + fae_util_path + "/openajax_a11y/scripts.txt\n")
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
        file_ws_urls.write(ws_url.url + '\n')    
      
    file_ws_urls.close()

  return

def analyzeWebsiteReport(ws_report, log):

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

  proc = subprocess.call(cmd, stdout=log)      
        
  page_count = countResultFiles(ws_report.data_directory + '/data')

  ave_time = "{:10.4f}".format(time.time()-start) + " seconds (0 pages)"
  if page_count > 0:
    if page_count == 1:
      ave_time = "{:10.4f}".format(time.time()-start) + " seconds/page (1 page)"
    else:  
      ave_time = "{:10.4f}".format((time.time()-start)/page_count) + " seconds/page (" + str(page_count) + " pages)"
  
  info("  Pages analyzed: " + str(page_count))
  info('Average processing time per page: ' + ave_time) 

class faeUtilThread(threading.Thread):
    def __init__(self, ws_report):
      threading.Thread.__init__(self)

      self.ws_report = ws_report
      info("=======================")
      info("Initializing report: " + self.ws_report.title)
      info("           log file: " + str(self.ws_report.log_file))
      self.ws_report.set_status_initialized()
      initWebsiteReport(self.ws_report)

    def run(self):

      log = open(self.ws_report.log_file, 'w')

      info("Analyze website: " + self.ws_report.title)
      self.ws_report.set_status_analyzing()
      analyzeWebsiteReport(self.ws_report, log)

      info("Saving Data: " + self.ws_report.title)
      self.ws_report.set_status_saving()
      saveResultsToDjango(self.ws_report, log)

      log.close()


def main():

  message_flag = True

  init_oaa_script_file()

  while True:  
    ws_reports = WebsiteReport.objects.filter(status="-")

    init_count = len(ws_reports)

    ws_analyzing = WebsiteReport.objects.filter(status="A")
    ws_saving    = WebsiteReport.objects.filter(status="S")

    processing_count = len(ws_analyzing) + len(ws_saving)

    if init_count and processing_count <= PROCESSING_THREADS:
      ws_report = ws_reports[0]

      thread = faeUtilThread(ws_report)
      thread.start()

      message_flag = True
    else:
      if message_flag:
        info("No report requests pending... ")
        info("Reports waiting: " + str(init_count))
        info("Reports running: " + str(processing_count))
        message_flag = False

      time.sleep(1)

          
if __name__ == "__main__":
  main()
