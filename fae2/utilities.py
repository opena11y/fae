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
"""

from __future__ import absolute_import
import re
# Formatter

from fae2.settings import STATIC_URL


def OAAMarkupToHTML(str):
  str1 = ""
  
  if str and len(str):
    str = str.replace("%s", "must")
  
    code = "<code>"
    for c in str:
      if c == '@':
        str1 += code;
        if code == "<code>":
          code = "</code>"
        else:
          code = "<code>"
      else:
        str1 += c      
  return str1

def OAAMarkupToText(str):
  str1 = ""

  if str and len(str):
    str = str.replace("%s", "must")
  
    for c in str:
      if c != '@':
        str1 += c    
          
  return str1



def HTMLToSourceCodeFormat(text):
    """A filter to format the sample HTML for rendering the soruce code"""
    try:
        out = re.sub(r'&','&amp;', text)
        out = re.sub(r'\t', '&#160;&#160;', out)
        out = re.sub(r'<', '&lt;', out)
        out = re.sub(r'>', '&gt;', out)
        out = re.sub(r'&lt;HL1&gt;', '<strong>', out)
        out = re.sub(r'&lt;/HL1&gt;', '</strong>', out)
        out = re.sub(r'&lt;HL2&gt;', '<em>', out)
        out = re.sub(r'&lt;/HL2&gt;', '</em>', out)
        out = re.sub(r'\n', '<br/>\n', out)
        out = re.sub(r'  ', '&#160;&#160;', out)
        out = re.sub(r'{{EXAMPLE_MEDIA}}',  STATIC_URL + 'examples/', out)
        return out
    except (TypeError, NameError, AttributeError):
        return ''


def OAAMarkupRemoveHighlightCode(text):

    """Remove tags for highlighting for rendering the code as HTML."""

    try:
        out = re.sub(r'<HL1>', '', text)
        out = re.sub(r'</HL1>', '', out)
        out = re.sub(r'<HL2>', '', out)
        out = re.sub(r'</HL2>', '', out)
        out = re.sub(r'{{EXAMPLE_MEDIA}}', STATIC_URL + 'examples/', out)
        return out
    except (TypeError, NameError, AttributeError):
        return ''

   
