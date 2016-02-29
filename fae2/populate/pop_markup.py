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

"""This file is for populating the database with markup information
I empty it. Run as a standalone script!"""

from markup.models import LanguageSpec
from markup.models import ElementDefinition

def create_spec(title, abbr, url, url_slug, link_text, flag):

  try:
    spec = LanguageSpec.objects.get(url_slug=url_slug)
    print("  Updating Spec: " + spec.url_slug )
    spec.title         = title
    spec.abbr          = abbr
    spec.url           = url
    spec.link_text     = link_text
    spec.element_based = flag
  except ObjectDoesNotExist:
    spec = LanguageSpec(title=title, abbr=abbr, url=url, url_slug=url_slug, link_text=link_text, element_based=flag)
    print("  Creating Testsuite Spec " + title) 
  spec.save()
  return spec
  
def create_element_definition(s, e, a, v, url, d, t):

  try:
    edef = ElementDefinition.objects.get(spec=s, element=e, attribute=a, value=v)
    if v == '':
      v = '*'
    print("  Updating ElementDefinition: " + str(s) + " for " + e + '[' + a + '=' + v + ']')
    edef.description = d
    edef.type = t
    edef.url = url
  except ObjectDoesNotExist:
    edef = ElementDefinition(spec=s, element=e, attribute=a, value=v, url=url, description=d, type=t)
    print("  Creating ElementDefinition: " + s.title  + " for " + url)
  edef.save()
  return edef

html = create_spec("HTML 4.01", "HTML 4.01", "http://www.w3.org/tr/html", "html4", "HTML4", True)

html_textnode       = create_element_definition( html, "textnodes",   "",  "", "http://www.w3.org/TR/html4/interact/scripts.html",   "", "")
html_all            = create_element_definition( html, "",   "",             "", "http://www.w3.org/TR/html4/",         "", "")

html_all_mousedown  = create_element_definition( html, "",   "onmousedown",  "", "http://www.w3.org/TR/html4/interact/scripts.html#adef-onmousdown",   "", "E")
html_all_mouseup    = create_element_definition( html, "",   "onmouseup",    "", "http://www.w3.org/TR/html4/interact/scripts.html#adef-onmousup",     "", "E")
html_all_mouseover  = create_element_definition( html, "",   "onmouseover",  "", "http://www.w3.org/TR/html4/interact/scripts.html#adef-onmouseover",  "", "E")
html_all_mouseout   = create_element_definition( html, "",   "onmouseout",   "", "http://www.w3.org/TR/html4/interact/scripts.html#adef-onmouseout",   "", "E")
html_all_mousemove  = create_element_definition( html, "",   "onmousemove",  "", "http://www.w3.org/TR/html4/interact/scripts.html#adef-onmouseout",   "", "E")
html_all_blur       = create_element_definition( html, "",   "onblur",       "", "http://www.w3.org/TR/html4/interact/scripts.html#adef-onblur",       "", "E")
html_all_focus      = create_element_definition( html, "",   "onfocus",      "", "http://www.w3.org/TR/html4/interact/scripts.html#adef-onfocus",      "", "E")
html_all_click      = create_element_definition( html, "",   "onclick",      "", "http://www.w3.org/TR/html4/interact/scripts.html#adef-onclick",      "", "E")
html_all_change     = create_element_definition( html, "",   "onchange",     "", "http://www.w3.org/TR/html4/interact/scripts.html#adef-onchange",     "", "E")

html_html_lang = create_element_definition( html, "html",  "lang",    "", "http://www.w3.org/TR/html4/struct/global.html#adef-lang",         "", "")
html_all_lang  = create_element_definition( html, "",      "lang",    "", "http://www.w3.org/TR/html4/struct/global.html#adef-lang",         "", "")

html_a              = create_element_definition( html, "a",    "",         "", "http://www.w3.org/TR/html4/struct/objects.html#edef-a",      "", "")
html_a_href         = create_element_definition( html, "a",    "href",     "", "http://www.w3.org/TR/html4/struct/objects.html#adef-href",      "", "")
html_area_href      = create_element_definition( html, "area", "href",     "", "http://www.w3.org/TR/html4/struct/objects.html#adef-href",      "", "")

html_object        = create_element_definition( html, "object",    "",         "", "http://www.w3.org/TR/html4/struct/objects.html#edef-object",      "", "")
html_applet        = create_element_definition( html, "applet",    "",         "", "http://www.w3.org/TR/html4/struct/objects.html#edef-applet",      "", "")
html_embed         = create_element_definition( html, "embed",    "",         "", "http://msdn.microsoft.com/en-us/library/ms535245%28v=vs.85%29.aspx",   "", "")


html_area         = create_element_definition( html, "area",   "",         "", "http://www.w3.org/TR/html4/struct/objects.html#edef-area",   "", "")
html_area_alt     = create_element_definition( html, "area",   "alt",      "", "http://www.w3.org/TR/html4/struct/objects.html#adef-alt",    "", "")
html_area_title   = create_element_definition( html, "area",   "title",    "", "http://www.w3.org/TR/html4/struct/objects.html#adef-alt",    "", "")
html_img          = create_element_definition( html, "img",    "",         "", "http://www.w3.org/TR/html4/struct/objects.html#edef-img",    "", "")
html_img_alt      = create_element_definition( html, "img",    "alt",      "", "http://www.w3.org/TR/html4/struct/objects.html#adef-alt",    "", "")
html_img_title    = create_element_definition( html, "img",    "title",    "", "http://www.w3.org/TR/html4/struct/global.html#adef-title",   "", "")
html_img_longdesc = create_element_definition( html, "img",    "longdesc", "",  "http://www.w3.org/TR/html4/struct/global.html#adef-longdesc",   "", "")

html_title     = create_element_definition( html, "title",  "",        "", "hhttp://www.w3.org/TR/html4/struct/global.html#edef-TITLE",      "", "")
html_h1        = create_element_definition( html, "h1",      "",        "", "hhttp://www.w3.org/TR/html4/struct/global.html#edef-H1",      "", "")
html_h2        = create_element_definition( html, "h2",   "",        "", "hhttp://www.w3.org/TR/html4/struct/global.html#edef-H2",      "", "")

html_h3        = create_element_definition( html, "h3",   "",        "", "hhttp://www.w3.org/TR/html4/struct/global.html#edef-H3",      "", "")

html_h4        = create_element_definition( html, "h4",   "",        "", "hhttp://www.w3.org/TR/html4/struct/global.html#edef-H4",      "", "")

html_h5        = create_element_definition( html, "h5",   "",        "", "hhttp://www.w3.org/TR/html4/struct/global.html#edef-H5",      "", "")

html_h6        = create_element_definition( html, "h6",   "",        "", "hhttp://www.w3.org/TR/html4/struct/global.html#edef-H6",      "", "")

html_all_id         = create_element_definition( html, "",        "id",      "",         "http://www.w3.org/TR/html4/struct/global.html#adef-id",   "", "")
html_input_title    = create_element_definition( html, "input",   "title",   "", "http://www.w3.org/TR/html4/",         "", "")
html_button         = create_element_definition( html, "button",  "",        "",         "http://www.w3.org/TR/html4/struct/global.html#edef-button",   "", "")
html_button_title   = create_element_definition( html, "button",  "title",   "",         "http://www.w3.org/TR/html4/struct/global.html#edef-button",   "", "")
html_input          = create_element_definition( html, "input",   "",        "",         "http://www.w3.org/TR/html4/struct/global.html#edef-input",    "", "")
html_input_button   = create_element_definition( html, "input",   "type",    "button",   "http://www.w3.org/TR/html4/struct/global.html#edef-input",    "", "")
html_input_submit   = create_element_definition( html, "input",   "type",    "submit",   "http://www.w3.org/TR/html4/struct/global.html#edef-input",    "", "")
html_input_reset    = create_element_definition( html, "input",   "type",    "reset",    "http://www.w3.org/TR/html4/struct/global.html#edef-input",    "", "")
html_input_text     = create_element_definition( html, "input",   "type",    "text",     "http://www.w3.org/TR/html4/struct/global.html#edef-input",    "", "")
html_input_password = create_element_definition( html, "input",   "type",    "password", "http://www.w3.org/TR/html4/struct/global.html#edef-input",    "", "")
html_input_checkbox = create_element_definition( html, "input",   "type",    "checkbox", "http://www.w3.org/TR/html4/struct/global.html#edef-input",    "", "")
html_input_radio    = create_element_definition( html, "input",   "type",    "radio",    "http://www.w3.org/TR/html4/struct/global.html#edef-input",    "", "")
html_input_file     = create_element_definition( html, "input",   "type",    "file",     "http://www.w3.org/TR/html4/struct/global.html#edef-input",    "", "")
html_input_image    = create_element_definition( html, "input",   "type",    "image",    "http://www.w3.org/TR/html4/struct/global.html#edef-input",    "", "")
html_input_image    = create_element_definition( html, "input",   "type",    "submit",    "http://www.w3.org/TR/html4/struct/global.html#edef-input",    "", "")
html_select         = create_element_definition( html, "select",   "",       "",         "http://www.w3.org/TR/html4/struct/global.html#edef-select",   "", "")
html_select_title   = create_element_definition( html, "select",   "title",  "",         "http://www.w3.org/TR/html4/struct/global.html#adef-title",    "", "")
html_textarea       = create_element_definition( html, "textarea", "",       "",         "http://www.w3.org/TR/html4/struct/global.html#edef-textarea", "", "")
html_textarea_title = create_element_definition( html, "textarea", "title",  "",         "http://www.w3.org/TR/html4/struct/global.html#adef-title",    "", "")
html_label          = create_element_definition( html, "label",    "",       "",         "http://www.w3.org/TR/html4/struct/global.html#edef-label",    "", "")
html_fieldset       = create_element_definition( html, "fieldset", "",       "",         "http://www.w3.org/TR/html4/struct/global.html#edef-fieldset", "", "")
html_legend         = create_element_definition( html, "legend",   "",       "",         "http://www.w3.org/TR/html4/struct/global.html#edef-legend",   "", "")

html_a_accesskey         = create_element_definition( html, "a",        "accesskey",  "", "http://www.w3.org/TR/html4/struct/objects.html#adef-accesskey",      "", "")
html_input_accesskey     = create_element_definition( html, "input",    "accesskey",  "", "http://www.w3.org/TR/html4/struct/objects.html#adef-accesskey",      "", "")
html_button_accesskey    = create_element_definition( html, "button",   "accesskey",  "", "http://www.w3.org/TR/html4/struct/objects.html#adef-accesskey",      "", "")
html_textarea_accesskey  = create_element_definition( html, "textarea", "accesskey",  "", "http://www.w3.org/TR/html4/struct/objects.html#adef-accesskey",      "", "")
html_select_accesskey    = create_element_definition( html, "select",   "accesskey",  "", "http://www.w3.org/TR/html4/struct/objects.html#adef-accesskey",      "", "")

html_table          = create_element_definition( html, "table",  "",         "",         "http://www.w3.org/TR/html4/struct/global.html#edef-table", "", "")
html_table_summary  = create_element_definition( html, "table",  "summary",  "",         "http://www.w3.org/TR/html4/struct/global.html#adef-summary", "", "")
html_td             = create_element_definition( html, "td",     "",         "",         "http://www.w3.org/TR/html4/struct/global.html#edef-td",      "", "")
html_th             = create_element_definition( html, "th",     "",         "",         "http://www.w3.org/TR/html4/struct/global.html#edef-th",      "", "")
html_th_id          = create_element_definition( html, "th",     "id",       "",         "http://www.w3.org/TR/html4/struct/global.html#adef-id",      "", "")
html_td_headers     = create_element_definition( html, "td",     "headers",  "",         "http://www.w3.org/TR/html4/struct/global.html#adef-headers", "", "")

html_frame          = create_element_definition( html, "frame",  "",        "",   "http://www.w3.org/TR/html4/struct/global.html#edef-frame",    "", "")
html_frame_title    = create_element_definition( html, "frame",  "title",   "",   "http://www.w3.org/TR/html4/struct/global.html#adef-title",    "", "")
html_iframe_title   = create_element_definition( html, "iframe", "title",   "",   "http://www.w3.org/TR/html4/struct/global.html#adef-title",    "", "")

html_b              = create_element_definition( html, "b",       "",  "",   "http://www.w3.org/TR/html4/struct/global.html#edef-b",    "", "")
html_i              = create_element_definition( html, "i",       "",  "",   "http://www.w3.org/TR/html4/struct/global.html#edef-i",    "", "")
html_u              = create_element_definition( html, "u",       "",  "",   "http://www.w3.org/TR/html4/struct/global.html#edef-b",    "", "")
html_font           = create_element_definition( html, "font",    "",  "",   "http://www.w3.org/TR/html4/struct/global.html#edef-font",    "", "")
html_marquee        = create_element_definition( html, "marquee", "",  "",   "",    "", "")
html_blink          = create_element_definition( html, "blink",   "",  "",   "",    "", "")

html5 = create_spec("html 5", "html 5", "http://www.whatwg.org/specs/web-apps/current-work/multipage/", "html5", "html5", True)

html5_nav      = create_element_definition( html5, "nav",      "", "", "http://www.whatwg.org/specs/web-apps/current-work/multipage/sections.html#the-nav-element",          "", "")
html5_article  = create_element_definition( html5, "article",  "", "", "http://www.whatwg.org/specs/web-apps/current-work/multipage/sections.html#the-article-element",      "", "")
html5_section  = create_element_definition( html5, "section",  "", "", "http://www.whatwg.org/specs/web-apps/current-work/multipage/sections.html#the-section-element",      "", "")
html5_main     = create_element_definition( html5, "main",     "", "", "http://www.whatwg.org/specs/web-apps/current-work/multipage/grouping-content.html#the-main-element", "", "")
html5_aside    = create_element_definition( html5, "aside",    "", "", "http://www.whatwg.org/specs/web-apps/current-work/multipage/sections.html#the-aside-element",        "", "")
html5_footer   = create_element_definition( html5, "footer",   "", "", "http://www.whatwg.org/specs/web-apps/current-work/multipage/sections.html#the-footer-element",       "", "")
html5_header   = create_element_definition( html5, "header",   "", "", "http://www.whatwg.org/specs/web-apps/current-work/multipage/sections.html#the-header-element",       "", "")

html5_figure      = create_element_definition( html5, "figure",     "", "", "http://www.whatwg.org/specs/web-apps/current-work/multipage/grouping-content.html#the-figure-element",   "", "")
html5_figcaption  = create_element_definition( html5, "figcaption", "", "", "http://www.whatwg.org/specs/web-apps/current-work/multipage/grouping-content.html#the-figcaption-element",   "", "")

html5_audio    = create_element_definition( html5, "audio", "", "", "http://www.whatwg.org/specs/web-apps/current-work/multipage/the-video-element.html#the-audio-element",   "", "")
html5_video    = create_element_definition( html5, "video", "", "", "http://www.whatwg.org/specs/web-apps/current-work/multipage/the-video-element.html#the-video-element",   "", "")
html5_track    = create_element_definition( html5, "track", "", "", "http://www.whatwg.org/specs/web-apps/current-work/multipage/the-video-element.html#the-track-element",   "", "")



aria = create_spec("Accessible Rich Internet Application Specification", "ARIA 1.0", "http://www.w3.org/TR/wai-aria/", "aria10", "ARIA 1.0", True)

aria_role              = create_element_definition( aria, "", "role", "", "http://www.w3.org/TR/wai-aria/roles", "User interface widget","R")
aria_role_widget       = create_element_definition( aria, "", "role", "widget", "http://www.w3.org/TR/wai-aria/roles", "User interface widget","R")
aria_role_alert        = create_element_definition( aria, "", "role", "alert", "http://www.w3.org/TR/wai-aria/roles#alert", "User interface widget","R")
aria_role_alertdialog  = create_element_definition( aria, "", "role", "alertdialog", "http://www.w3.org/TR/wai-aria/roles#alertdialog", "User interface widget","R")
aria_role_button       = create_element_definition( aria, "", "role", "button", "http://www.w3.org/TR/wai-aria/roles#button", "User interface widget","R")
aria_role_checkbox     = create_element_definition( aria, "", "role", "checkbox", "http://www.w3.org/TR/wai-aria/roles#checkbox", "User interface widget","R")
aria_role_combobox     = create_element_definition( aria, "", "role", "combobox", "http://www.w3.org/TR/wai-aria/roles#combobox", "User interface widget","R")
aria_role_dialog       = create_element_definition( aria, "", "role", "dialog", "http://www.w3.org/TR/wai-aria/roles#dialog", "User interface widget","R")
aria_role_grid         = create_element_definition( aria, "", "role", "grid", "http://www.w3.org/TR/wai-aria/roles#grid", "Composite user interface widget","R")
aria_role_gridcell     = create_element_definition( aria, "", "role", "gridcell", "http://www.w3.org/TR/wai-aria/roles#gridcell", "User interface widget","R")
aria_role_link         = create_element_definition( aria, "", "role", "link", "http://www.w3.org/TR/wai-aria/roles#link", "User interface widget","R")
aria_role_listbox      = create_element_definition( aria, "", "role", "listbox", "http://www.w3.org/TR/wai-aria/roles#listbox", "Composite user interface widget","R")
aria_role_log          = create_element_definition( aria, "", "role", "log", "http://www.w3.org/TR/wai-aria/roles#log", "User interface widget","R")
aria_role_marquee      = create_element_definition( aria, "", "role", "marquee", "http://www.w3.org/TR/wai-aria/roles#marquee", "User interface widget","R")
aria_role_menu         = create_element_definition( aria, "", "role", "menu", "http://www.w3.org/TR/wai-aria/roles#menu", "Composite user interface widget","R")
aria_role_menubar      = create_element_definition( aria, "", "role", "menubar", "http://www.w3.org/TR/wai-aria/roles#menubar", "Composite user interface widget","R")
aria_role_menuitem     = create_element_definition( aria, "", "role", "menuitem", "http://www.w3.org/TR/wai-aria/roles#menuitem", "User interface widget","R")
aria_role_menuitemcheckbox = create_element_definition( aria, "", "role", "menuitemcheckbox", "http://www.w3.org/TR/wai-aria/roles#menuitemcheckbox", "User interface widget","R")
aria_role_menuitemradio    = create_element_definition( aria, "", "role", "menuitemradio", "http://www.w3.org/TR/wai-aria/roles#menuitemradio", "User interface widget","R")
aria_role_option       = create_element_definition( aria, "", "role", "option", "http://www.w3.org/TR/wai-aria/roles#option", "User interface widget","R")
aria_role_progressbar  = create_element_definition( aria, "", "role", "progressbar", "http://www.w3.org/TR/wai-aria/roles#progressbar", "User interface widget","R")
aria_role_radio        = create_element_definition( aria, "", "role", "radio", "http://www.w3.org/TR/wai-aria/roles#radio", "User interface widget","R")
aria_role_radiogroup   = create_element_definition( aria, "", "role", "radiogroup", "http://www.w3.org/TR/wai-aria/roles#radiogroup", "User interface widget","R")
aria_role_scrollbar    = create_element_definition( aria, "", "role", "scrollbar", "http://www.w3.org/TR/wai-aria/roles#scrollbar", "User interface widget","R")
aria_role_slider       = create_element_definition( aria, "", "role", "slider", "http://www.w3.org/TR/wai-aria/roles#slider", "User interface widget","R")
aria_role_spinbutton   = create_element_definition( aria, "", "role", "spinbutton", "http://www.w3.org/TR/wai-aria/roles#spinbutton", "User interface widget","R")
aria_role_status       = create_element_definition( aria, "", "role", "status", "http://www.w3.org/TR/wai-aria/roles#status", "User interface widget","R")
aria_role_tab          = create_element_definition( aria, "", "role", "tab", "http://www.w3.org/TR/wai-aria/roles#tab", "User interface widget","R")
aria_role_tabpanel     = create_element_definition( aria, "", "role", "tabpanel", "http://www.w3.org/TR/wai-aria/roles#tabpanel", "User interface widget","R")
aria_role_textbox      = create_element_definition( aria, "", "role", "textbox", "http://www.w3.org/TR/wai-aria/roles#textbox", "User interface widget","R")
aria_role_timer        = create_element_definition( aria, "", "role", "timer", "http://www.w3.org/TR/wai-aria/roles#timer", "User interface widget","R")
aria_role_tooltip      = create_element_definition( aria, "", "role", "tooltip", "http://www.w3.org/TR/wai-aria/roles#tooltip", "User interface widget","R")
aria_role_treeitem     = create_element_definition( aria, "", "role", "treeitem", "http://www.w3.org/TR/wai-aria/roles#treeitem", "User interface widget","R")
aria_role_tablist      = create_element_definition( aria, "", "role", "tablist", "http://www.w3.org/TR/wai-aria/roles#tablist", "Composite user interface widget","R")
aria_role_toolbar      = create_element_definition( aria, "", "role", "toolbar", "http://www.w3.org/TR/wai-aria/roles#toolbar", "Composite user interface widget","R")
aria_role_tree         = create_element_definition( aria, "", "role", "tree", "http://www.w3.org/TR/wai-aria/roles#tree", "Composite user interface widget","R")
aria_role_treegrid     = create_element_definition( aria, "", "role", "treegrid", "http://www.w3.org/TR/wai-aria/roles#treegrid", "Composite user interface widget","R")
aria_role_article      = create_element_definition( aria, "", "role", "article", "http://www.w3.org/TR/wai-aria/roles#article", "Document structure","R")
aria_role_columnheader = create_element_definition( aria, "", "role", "columnheader", "http://www.w3.org/TR/wai-aria/roles#columnheader", "Document structure","R")
aria_role_definition   = create_element_definition( aria, "", "role", "definition", "http://www.w3.org/TR/wai-aria/roles#definition", "Document structure","R")
aria_role_directory    = create_element_definition( aria, "", "role", "directory", "http://www.w3.org/TR/wai-aria/roles#directory", "Document structure","R")
aria_role_document     = create_element_definition( aria, "", "role", "document", "http://www.w3.org/TR/wai-aria/roles#document", "Document structure","R")
aria_role_group        = create_element_definition( aria, "", "role", "group", "http://www.w3.org/TR/wai-aria/roles#group", "Document structure","R")
aria_role_heading      = create_element_definition( aria, "", "role", "heading", "http://www.w3.org/TR/wai-aria/roles#heading", "Document structure","R")
aria_role_img          = create_element_definition( aria, "", "role", "img", "http://www.w3.org/TR/wai-aria/roles#img", "Document structure","R")
aria_role_list         = create_element_definition( aria, "", "role", "list", "http://www.w3.org/TR/wai-aria/roles#list", "Document structure","R")
aria_role_listitem     = create_element_definition( aria, "", "role", "listitem", "http://www.w3.org/TR/wai-aria/roles#listitem", "Document structure","R")
aria_role_math         = create_element_definition( aria, "", "role", "math", "http://www.w3.org/TR/wai-aria/roles#math", "Document structure","R")
aria_role_note         = create_element_definition( aria, "", "role", "note", "http://www.w3.org/TR/wai-aria/roles#note", "Document structure","R")
aria_role_presentation = create_element_definition( aria, "", "role", "presentation", "http://www.w3.org/TR/wai-aria/roles#presentatin", "Document structure","R")
aria_role_region       = create_element_definition( aria, "", "role", "region", "http://www.w3.org/TR/wai-aria/roles#region", "Document structure","R")
aria_role_row          = create_element_definition( aria, "", "role", "row", "http://www.w3.org/TR/wai-aria/roles#row", "Document structure","R")
aria_role_rowgroup     = create_element_definition( aria, "", "role", "rowgroup", "http://www.w3.org/TR/wai-aria/roles#rowgroup", "Document structure","R")
aria_role_rowheader    = create_element_definition( aria, "", "role", "rowheader", "http://www.w3.org/TR/wai-aria/roles#rowheader", "Document structure","R")
aria_role_separator    = create_element_definition( aria, "", "role", "separator", "http://www.w3.org/TR/wai-aria/roles#separator", "Document structure","R")
aria_role_application  = create_element_definition( aria, "", "role", "application", "http://www.w3.org/TR/wai-aria/roles#application", "Landmark","R")
aria_role_banner       = create_element_definition( aria, "", "role", "banner", "http://www.w3.org/TR/wai-aria/roles#banner", "Landmark","R")
aria_role_complementary = create_element_definition( aria, "", "role", "complementary", "http://www.w3.org/TR/wai-aria/roles#complementary", "Landmark","R")
aria_role_contentinfo   = create_element_definition( aria, "", "role", "contentinfo", "http://www.w3.org/TR/wai-aria/roles#contentinfo", "Landmark","R")
aria_role_form          = create_element_definition( aria, "", "role", "form", "http://www.w3.org/TR/wai-aria/roles#form", "Landmark","R")
aria_role_main          = create_element_definition( aria, "", "role", "main", "http://www.w3.org/TR/wai-aria/roles#main", "Landmark","R")
aria_role_navigation    = create_element_definition( aria, "", "role", "navigation", "http://www.w3.org/TR/wai-aria/roles#navigation", "Landmark","R")
aria_role_search        = create_element_definition( aria, "", "role", "search", "http://www.w3.org/TR/wai-aria/roles#search", "Landmark","R")
aria_atomic           = create_element_definition( aria, "", "aria-atomic", "", "http://www.w3.org/TR/wai-aria/states_and_properties#aria-atomic", "Live region attribute","P")
aria_busy             = create_element_definition( aria, "", "aria-busy", "", "http://www.w3.org/TR/wai-aria/states_and_properties#aria-busy", "Live region attribute","S")
aria_live             = create_element_definition( aria, "", "aria-live", "", "http://www.w3.org/TR/wai-aria/states_and_properties#aria-live", "Global state or property","P")
aria_relevant         = create_element_definition( aria, "", "aria-relevant", "", "http://www.w3.org/TR/wai-aria/states_and_properties#aria-relevant", "Global state or property","P")
aria_autocomplete     = create_element_definition( aria, "", "aria-autocomplete", "", "http://www.w3.org/TR/wai-aria/states_and_properties#aria-autocomplete", "Widget attributes","P")
aria_checked          = create_element_definition( aria, "", "aria-checked", "", "http://www.w3.org/TR/wai-aria/states_and_properties#aria-checked", "Widget attributes","S")
aria_disabled         = create_element_definition( aria, "", "aria-disabled", "", "http://www.w3.org/TR/wai-aria/states_and_properties#aria-disabled", "Widget attributes","S")
aria_expanded         = create_element_definition( aria, "", "aria-expanded", "", "http://www.w3.org/TR/wai-aria/states_and_properties#aria-expanded", "Widget attributes","S")
aria_haspopup         = create_element_definition( aria, "", "aria-haspopup", "", "http://www.w3.org/TR/wai-aria/states_and_properties#aria-haspopup", "Widget attributes","P")
aria_hidden           = create_element_definition( aria, "", "aria-hidden", "", "http://www.w3.org/TR/wai-aria/states_and_properties#aria-hidden", "Widget attributes","S")
aria_invalid          = create_element_definition( aria, "", "aria-invalid", "", "http://www.w3.org/TR/wai-aria/states_and_properties#aria-invalid", "Widget attributes","S")
aria_label            = create_element_definition( aria, "", "aria-label", "", "http://www.w3.org/TR/wai-aria/states_and_properties#aria-label", "Widget attributes","P")
aria_level            = create_element_definition( aria, "", "aria-level", "", "http://www.w3.org/TR/wai-aria/states_and_properties#aria-level", "Widget attributes","P")
aria_multiline        = create_element_definition( aria, "", "aria-multiline", "", "http://www.w3.org/TR/wai-aria/states_and_properties#aria-multiline", "Widget attributes","P",)
aria_multiselectable  = create_element_definition( aria, "", "aria-multiselectable", "", "http://www.w3.org/TR/wai-aria/states_and_properties#aria-multiselectable", "Widget attributes","P")
aria_orientation      = create_element_definition( aria, "", "aria-orientation", "", "http://www.w3.org/TR/wai-aria/states_and_properties#aria-orientation", "Widget attributes","P")
aria_pressed          = create_element_definition( aria, "", "aria-pressed", "", "http://www.w3.org/TR/wai-aria/states_and_properties#aria-pressed", "Widget attributes","S")
aria_readonly         = create_element_definition( aria, "", "aria-readonly", "", "http://www.w3.org/TR/wai-aria/states_and_properties#aria-readonly", "Widget attributes","P")
aria_required         = create_element_definition( aria, "", "aria-required", "", "http://www.w3.org/TR/wai-aria/states_and_properties#aria-required", "Widget attributes","P")
aria_selected         = create_element_definition( aria, "", "aria-selected", "", "http://www.w3.org/TR/wai-aria/states_and_properties#aria-selected", "Widget attributes","S")
aria_sort             = create_element_definition( aria, "", "aria-sort", "", "http://www.w3.org/TR/wai-aria/states_and_properties#aria-sort", "Widget attributes","P")
aria_valuemax         = create_element_definition( aria, "", "aria-valuemin", "", "http://www.w3.org/TR/wai-aria/states_and_properties#aria-valuemin", "Widget attributes","P")
aria_valuemin         = create_element_definition( aria, "", "aria-valuemax", "", "http://www.w3.org/TR/wai-aria/states_and_properties#aria-valuemax", "Widget attributes","P")
aria_valuenow         = create_element_definition( aria, "", "aria-valuenow", "", "http://www.w3.org/TR/wai-aria/states_and_properties#aria-valuenow", "Widget attributes","P")
aria_valuetext        = create_element_definition( aria, "", "aria-valuetext", "", "http://www.w3.org/TR/wai-aria/states_and_properties#aria-valuetext", "Widget attributes","P")
aria_dropeffect       = create_element_definition( aria, "", "aria-dropeffect", "", "http://www.w3.org/TR/wai-aria/states_and_properties#aria-dropeffect", "Drag and drop attributes","P")
aria_grabbed          = create_element_definition( aria, "", "aria-grabbed", "", "http://www.w3.org/TR/wai-aria/states_and_properties#aria-grabbed", "Drag and drop attributes",'S')
aria_activedescendant = create_element_definition( aria, "", "aria-activedescendant", "", "http://www.w3.org/TR/wai-aria/states_and_properties#aria-activedescendant", "Relationship attributes","P")
aria_controls         = create_element_definition( aria, "", "aria-controls", "", "http://www.w3.org/TR/wai-aria/states_and_properties#aria-controls", "Relationship attributes","P")
aria_describedby      = create_element_definition( aria, "", "aria-describedby", "", "http://www.w3.org/TR/wai-aria/states_and_properties#aria-describedby", "Relationship attributes","P")
aria_flowto           = create_element_definition( aria, "", "aria-flowto", "", "http://www.w3.org/TR/wai-aria/states_and_properties#aria-flowto", "Relationship attributes","P")
aria_labelledby       = create_element_definition( aria, "", "aria-labelledby", "", "http://www.w3.org/TR/wai-aria/states_and_properties#aria-labelledby", "Relationship attributes","P")
aria_owns             = create_element_definition( aria, "", "aria-owns", "", "http://www.w3.org/TR/wai-aria/states_and_properties#aria-owns", "Relationship attributes","P")
aria_posinset         = create_element_definition( aria, "", "aria-posinset", "", "http://www.w3.org/TR/wai-aria/states_and_properties#aria-posinset", "Relationship attributes","P")
aria_setsize          = create_element_definition( aria, "", "aria-setsize", "", "http://www.w3.org/TR/wai-aria/states_and_properties#aria-setsize", "Relationship attributes","P")

css = create_spec("CSS 2.1", "CSS 2.1", "http://www.w3.org/tr/css21", "css21", "CSS21", False)

css_position   = create_element_definition( css, "position", "", "", "http://www.w3.org/TR/CSS21/visuren.html#propdef-position", "","O")
css_left       = create_element_definition( css, "left",     "", "", "http://www.w3.org/TR/CSS21/visuren.html#propdef-left", "","O")
css_right      = create_element_definition( css, "right",    "", "", "http://www.w3.org/TR/CSS21/visuren.html#propdef-right", "","O")
css_top        = create_element_definition( css, "top",      "", "", "http://www.w3.org/TR/CSS21/visuren.html#propdef-top", "","O")
css_bottom     = create_element_definition( css, "bottom",   "", "", "http://www.w3.org/TR/CSS21/visuren.html#propdef-bottom", "","O")
css_float      = create_element_definition( css, "float",    "", "", "http://www.w3.org/TR/CSS21/visuren.html#propdef-float", "","O")
css_clear      = create_element_definition( css, "clear",    "", "", "http://www.w3.org/TR/CSS21/visuren.html#propdef-clear", "","O")
css_color         = create_element_definition( css, "color",          "", "", "http://www.w3.org/TR/CSS21/visuren.html#propdef-color",         "", 'C')
css_background    = create_element_definition( css, "background",     "", "", "http://www.w3.org/TR/CSS21/visuren.html#propdef-background",    "", 'C')
css_border_color  = create_element_definition( css, "border-color",   "", "", "http://www.w3.org/TR/CSS21/visuren.html#propdef-border-color",  "", 'C')
css_outline_color = create_element_definition( css, "outline-color",  "", "", "http://www.w3.org/TR/CSS21/ui.html#propdef-outline-color",      "", 'C')
css_font          = create_element_definition( css, "font",           "", "", "http://www.w3.org/TR/CSS21/visuren.html#propdef-font",          "", 'F')
css_font_size     = create_element_definition( css, "font-size",      "", "", "http://www.w3.org/TR/CSS21/ui.html#propdef-font-family",        "", 'F')
css_content       = create_element_definition( css, "content",      "", "", "http://www.w3.org/TR/CSS21/ui.html#propdef-content",        "", 'O')

css_focus         = create_element_definition( css, ":focus",  "", "", "http://www.w3.org/TR/CSS21/selector.html#x38",        "", 'H')
css_hover         = create_element_definition( css, ":hover",  "", "", "http://www.w3.org/TR/CSS21/selector.html#x38",        "", 'H')
css_active        = create_element_definition( css, ":active", "", "", "http://www.w3.org/TR/CSS21/selector.html#x38",        "", 'H')

    