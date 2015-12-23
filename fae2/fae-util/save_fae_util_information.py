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

sys.path.append(os.path.abspath('..'))

from django.utils.encoding  import iri_to_uri

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fae2.settings')
from django.conf import settings

from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.models import User

from reports.models import ProcessedURL, FilteredURL, UnprocessedURL

# from usage.models import Usage

from django.db import connection, transaction


DEBUG=False
INFO=True
ERROR=True

def debug(s):
  if DEBUG:
    print ("[SAVE UTIL   ][debug  ]: " + str(s))

def info(s):
  if INFO:
    print ("[SAVE UTIL   ][Info   ]: " + str(s))

def error(s):
  if ERROR:
    print ("[SAVE UTIL   ][**ERROR]: " + str(s))
    

    
def stripQuotes(s):
  if s.startswith('"') and s.endswith('"'):
    s = s[1:-1]  
  return s    

def statusToDatabase(ws_report, file_status):
  # get usage object corresponding to ws_report
  
  try: 
    #create usage object
    un    = ws_report.user.username
    rs_id = ws_report.ruleset.ruleset_id
        
    usage = Usage(username=un, ruleset_id=rs_id, ws_report_id=ws_report.id)  
    usage.save()
  except:
    usage = False
    error("Error creating usage file for: " + str(ws_report))
    
  for line in file_status:
    parts = line.split('=')
    if len(parts) == 2:
      if parts[0] == 'processed':
        ws_report.processed_urls_count   = int(parts[1])  
        if usage:
          usage.processed_urls_count   = int(parts[1])
      elif parts[0] == 'unprocessed':      
        ws_report.unprocessed_urls_count = int(parts[1]) 
        if usage:
          usage.unprocessed_urls_count   = int(parts[1]) 
      elif parts[0] == 'filtered':      
        ws_report.filtered_urls_count    = int(parts[1]) 
        if usage:
          usage.filtered_urls_count    = int(parts[1])  
      elif parts[0] == 'time':
        ws_report.processing_time = int(float(parts[1])*1000.0)
        if usage:
          usage.processing_time = int(float(parts[1])*1000.0)
            
  try:      
    ws_report.save()    
    if usage:
      usage.save()
  except:
    error("** Error: Could not update status information")
        
def getRowWithComplicatedURLs(r, n):     

  debug("    Complicated Row: " + r)
  r_len = len(r)

  items = []
  
  pos0 = r.find('"', 0, r_len)
  if pos0 < 0:
    return [] 
  
  if pos0 != 0:
    item = r[0:(pos0-1)] 
    debug("       First Number: " + item)
    items.append(item)
  else:
    pos = 0  

  pos1 = r.find('","http', (pos0+1), r_len) 
  if pos1 < 0:
    return []   
    
  url1 = r[pos0:(pos1+1)]
  items.append(url1)

  pos2 = r.find('","http', (pos1+6), r_len) 
  if pos2 < 0:
    pos2 = r.find('",', (pos1+6), r_len)
    if pos2 < 0:
      return []

  url2 = r[(pos1+2):(pos2+1)]
  items.append(url2)

  url3 = "none"
  pos3 = r.find('",', (pos2+6), r_len) 
  if pos3 > 0:
    url3 = r[(pos2+2):(pos3+1)]
    items.append(url3)
    pos2 = pos3

  r1 = r[(pos2+2):r_len]
  
  if len(r1) > 0:
    r1 = r1.strip()
  
  debug("   Complicated URL 1: " + url1)
  debug("   Complicated URL 2: " + url2)
  debug("   Complicated URL 3: " + url3)
  debug("Complicated Remander: " + r1 + " (" + str(len(r1)) + ")")
  
  if len(r1):    
    r2 = r1.split(",")

    for item in r2:
      items.append(item)   
     
  if len(items) == n:
    return items
    
  return []

def filteredUrlsToDatabase(ws_report, fname, num):
  
  def getRowItems(r):
    items = row.split(',')
      
    # if the row is clean of extra commas then there should be the n items
    if len(items) == num:
      return items

    # there are more than n-1 commas so URLs are complicated, probably have javascript code in them         
    items = getRowWithComplicatedURLs(r, num)
      
    if len(items) == num:
      return items
             
    return []  

  info("Filtered urls from: " + fname)   
    
  try:    
    with open(fname, 'r') as csvfile:     

      i = 1
      try: 
        for row in csvfile:
          debug("  Row: " + row)

          items = getRowItems(row)
          
          if len(items) == num:  
            url1 = iri_to_uri(stripQuotes(items[0]))
            url2 = iri_to_uri(stripQuotes(items[1][:-1]))
            i += 1
            try:
              o_url = FilteredURL(ws_report=ws_report, url=url1, url_referenced=url2)
              o_url.save()
            except:   
              error("** Error saving FilteredURL object for: " + " " + url1 + " from  " + url2)
          else:    
            error("** Could not parse row into " + str(num) + " parts: " + row)
      except:
        error("** Error reading csv formatted file line: " + str(i) + " in " + fname)           
  except IOError as e:
    error("******** Error: " + fname + " cannot be opened")
    error("  I/O error({0}): {1}".format(e.errno, e.strerror))    
      
def unprocessedUrlsToDatabase(ws_report, fname, num):
  
  def getRowItems(r):
    items = row.split(',')
    
    # if the row is clean of extra commas then there should be the n items
    if len(items) == num:
      return items

    # there are more than n-1 commas so URLs are complicated, probably have javascript code in them       
    items = getRowWithComplicatedURLs(r, num)
    
    if len(items) == num:
      return items
         
    return []  

  info("Unprocessed urls from: " + fname)   
  
  try:  
  
    with open(fname, 'r') as csvfile:   
      i = 1
      try: 
        for row in csvfile:
          debug('  ROW: ' + row)

          items = getRowItems(row)
        
          if len(items) == num:  
            url1 = iri_to_uri(stripQuotes(items[0]))
            url2 = iri_to_uri(stripQuotes(items[1]))
            i += 1
            try:
              up_url = UnprocessedURL(ws_report=ws_report, url=url1, url_referenced=url2)
              up_url.dom_time   = int(items[2]) 	
              up_url.link_time  = int(items[3])	
              up_url.event_time = int(items[4])	
              up_url.eval_time  = int(items[5]) 	
              up_url.save_time  = int(items[6])	
              up_url.total_time = int(items[2]) + int(items[3]) + int(items[4]) + int(items[5]) + int(items[6])
              up_url.save()
            except:   
              error("** Error creating UnprocessedURL object for: " + url1 + " from  " + url2)
          else:    
            error("** Could not parse row into " + str(num) + " parts: " + row)
      except:
        error("** Error reading csv formatted file line: " + str(i) + " in " + fname)         
        
  except IOError as e:
    error("******** Error: " + fname + " cannot be opened")
    error("  I/O error({0}): {1}".format(e.errno, e.strerror))    

def processedUrlsToDatabase(ws_report, fname, num):
  
  def getRowItems(r):
    
    items = r.split(',')

    # if the line contains simple URLs there should be only 7 commas
    if len(items) == num:
      return items

    # there are more than 7 commas so URLs are complicated, probably have javascript code in them       
    items = getRowWithComplicatedURLs(r, num)
    
    if len(items) == num:
      return items
    
    return []   
  
  info("Processed urls from: " + fname)   
  try: 
    with open(fname, 'r') as csvfile:     
        
      i = 1
      try: 
        for row in csvfile:
          debug('  ROW: ' + row)
          items = getRowItems(row)
        
          if len(items) == num:
            url1 = iri_to_uri(stripQuotes(items[1]))
            url2 = iri_to_uri(stripQuotes(items[2]))
            url3 = iri_to_uri(stripQuotes(items[3]))
#            info("  URLS: " + items[0] + " url1: " + url1 + " url2: " + url2 + " url3: " + url3)
            try:
              p_url = ProcessedURL(ws_report=ws_report, url_requested=url1, url_returned=url2, url_referenced=url3)
              p_url.page_seq_num     = int(items[0])
              p_url.redirect         = (url1 != url2)
              p_url.http_status_code = int(items[4]) 	
              p_url.dom_time         = int(items[5]) 	
              p_url.link_time        = int(items[6])	
              p_url.event_time       = int(items[7])	
              p_url.eval_time        = int(items[8]) 	
              p_url.save_time        = int(items[9])	
              p_url.total_time       = int(items[5]) + int(items[6]) + int(items[7]) + int(items[8]) + int(items[9])
              p_url.save()
              i += 1
            except:   
              error("** Error creating ProcessedURL object for: " + items[0] + " " + url1 + " from  " + url2)
          else:    
            error("** Could not parse row into " + str(num) + " parts: " + row)
      except:
        error("** Error reading line: " + str(i) + " in " + fname)                           
  except IOError as e:
    error("******** Error: " + fname + " cannot be opened")
    error("  I/O error({0}): {1}".format(e.errno, e.strerror))    

