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

file: populate/pop_rules.py

Author: Jon Gunderson

"""

from __future__ import print_function
from __future__ import absolute_import
import sys
import os
import django
from django.core.exceptions import ObjectDoesNotExist
import re

fp = os.path.realpath(__file__)
path, filename = os.path.split(fp)

fae2_path = path.split('/populate')[0]
sys.path.append(fae2_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fae2.settings')
from django.conf import settings

django.setup()

import json

from abouts.models           import FAQ

def addFAQ(seq, title, description):

  try:   
    faq = FAQ.objects.get(seq=seq)
    print("Updated FAQ: " + title)
    faq.title = title
    faq.description = description
  except:
    print("Created FAQ: " + title)
    faq = FAQ(seq=seq, title=title, description=description)

  faq.save()

desc = """
There are two major reasons why FAE 2.0 and AInspector Sidebar evaluation results may be different:

1. When a page includes dynamically loaded content, the DOM that FAE 2.0 sees will often be different from the DOM that AInspector Sidebar sees, resulting in different evaluation results.  The more dynamic the content in the page, the more possibility of a discrepancy.   
1. Pages that are responsive to screen dimensions will have different content rendered depending on the width of the screen.  FAE 2.0 generally has a wide screen and AInspector Sidebar will analyze the content based on the current screen width.

Note: AInspector Sidebar will generally be more accurate than FAE for looking at Individual Pages.

"""

addFAQ(1, "Why are the FAE 2.0 and AInspector Sidebar evaluation results different?", desc)  

