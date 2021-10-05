"""
Copyright 2014-2021 University of Illinois

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

file: populate/pop_wcag20.py

Author: Jon Gunderson

"""

from __future__ import print_function
from __future__ import absolute_import
import sys
import os
import django
from django.core.exceptions import ObjectDoesNotExist

fp = os.path.realpath(__file__)
path, filename = os.path.split(fp)

fae2_path = path.split('/populate')[0]
sys.path.append(fae2_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fae2.settings')
from django.conf import settings

django.setup()

from wcag20.models import Principle, Guideline, SuccessCriterion

"""This file is for populating the database with WCAG 2.0 References"""

# Principle.objects.all().delete()
# Guideline.objects.all().delete()
# SuccessCriterion.objects.all().delete()

import json
json_data=open(os.path.join(path,'wcag.json'))
data = json.load(json_data)
json_data.close()

def wcag_principle(num, title, url):
  try:
    principle = Principle.objects.get(num=num)
    print("  " + title + " (found)")

    principle.title = title
    principle.url = url
    print("  " + title + " (updated) ")

  except:
    principle = Principle(num=num, title=ttile, url=url)
    print("  " + principle.title + " (CREATED)")

  principle.save()

  return principle

def wcag_guideline(p_obj, num, title, url, slug):
  try:
    guideline       = Guideline.objects.get(principle=p_obj, num=num)
    print("    " +  title + " (found)")
    guideline.title = title
    guideline.url   = url
    guideline.slug  = 'p' + str(p_obj.num) + 'g' + str(num)
    print("    " + title + " (updated)")

  except:
    guideline = Guideline(principle=p_obj, num=num, title=title, url=url, slug=slug)
    print("    " + title + " (CREATED)")

  guideline.save()

  return guideline

def wcag_success_criterion(g_obj, num, title, level, url, url_meet, url_understand, slug):
  try:
    sc = SuccessCriterion.objects.get(guideline=g_obj, num=num)
    print("      " +  title + " (found)")
    sc.title    = title
    sc.url      = url
    sc.url_meet = url_meet
    sc.url_understand = url_understand
    sc.level    = level
    sc.slug     = g_obj.slug + 'sc' + str(num)
    print("    " + title + " (updated)")
  except:
    sc = SuccessCriterion(guideline=g_obj, num=num, title=title, url=url, url_meet=url_meet, url_understand=url_understand, level=level, slug=slug)
    print("    " + title  + " (CREATED)")

  sc.save()

  return sc

def wcag():
  for p in data['principles']:
    print('[Principle]: ' + p);
    p_data = data['principles'][p];

    p_num = int(p)
    p_title = p_data['title']
    p_url = p_data['url_spec'];
    p_obj = wcag_principle(p_num, p_title, p_url);

    for g in p_data['guidelines']:
      print('  [Guideline]: ' + p);
      g_data = p_data['guidelines'][g];

      g_num   = int(g.split('.')[1])
      g_title = g_data['title']
      g_url   = g_data['url_spec'];
      g_slug  = g_url.split('#')[1];

      # currently do not support rules for Guideline 2.5
      if p_num == 2 and g_num >= 5:
        continue

      g_obj = wcag_guideline(p_obj, g_num, g_title, g_url, g_slug);

      for sc in g_data['success_criteria']:
        print('    [Success Criteria]: ' + sc);
        sc_data = g_data['success_criteria'][sc];

        sc_num      = int(sc.split('.')[2])
        sc_title    = sc_data['title']
        sc_url      = sc_data['url_spec'];
        sc_url_meet = sc_data['url_meet'];
        sc_url_understand = sc_data['url_understand'];
        sc_slug     = sc_url.split('#')[1];

        sc_level    = sc_data['level'];
        if sc_level.find('AAA') >= 0:
          sc_level = '3';
        else:
          if sc_level.find('AA') >= 0:
            sc_level = '2';
          else:
            sc_level = '1';

#        print('  [    num]: ' + str(sc_num))
#        print('  [  title]: ' + sc_title)
#        print('  [  level]: ' + sc_level)
#        print('  [    url]: ' + sc_url)
#        print('  [   meet]: ' + sc_url_meet)
#        print('  [underst]: ' + sc_url_understand)
#        print('  [   slug]: ' + sc_slug)

        if len(sc_slug) > 32:
          sc_slug = sc_slug[0:32]

        wcag_success_criterion(g_obj, sc_num, sc_title, sc_level, sc_url, sc_url_meet, sc_url_understand, sc_slug);

wcag()
