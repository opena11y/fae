import sys,os
import django
from django.core.exceptions import ObjectDoesNotExist

sys.path.append(os.path.abspath('..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fae2.settings')
from django.conf import settings

django.setup()

import json

from rules.models           import Rule
from rules.models           import RuleScope
from rules.models           import RuleGroup
from rules.models           import NodeResultMessage
from rules.models           import InformationalLink
from ruleCategories.models  import RuleCategory
from techniques.models      import Technique
from manualChecks.models    import ManualCheck
from wcag20.models          import WCAG20_SuccessCriterion
from markup.models          import ElementDefinition

from django.contrib.auth.models import User

json_data=open('oaa_exported_rules.json')

data = json.load(json_data)

json_data.close()

# Rule.objects.all().delete()
# ManualCheck.objects.all().delete()
# Technique.objects.all().delete()
# InformationalLink.objects.all().delete()

def addTechnique(rule, id, title, url, date):
  if title != "":
    if url != "":
      tech = Technique(rule=rule, technique_id=id, title=title, url=url, updated_date=date)
    else:  
      tech = Technique(rule=rule, technique_id=id, title=title, updated_date=date)
    tech.save()

def addManualCheck(rule, title, url, date):
  if title != "": 
    if url != "":
      mc = ManualCheck(rule=rule, title=title, url=url, updated_date=date)
    else:  
      mc = ManualCheck(rule=rule, title=title, updated_date=date)
    mc.save()

def addInformationalLink(rule, type, title, url, date):
  print("  Information link title: " + title)
  print("  Information link url:   " + url)
  if title != "": 
    if url != "":
      il = InformationalLink(rule=rule, type=str(type), title=title, url=url, updated_date=date)
    else:  
      il = InformationalLink(rule=rule, type=str(type), title=title, updated_date=date)
    il.save()

def addRuleResultMessage(rule, label, message, date):
  print("  Rule Result Message: " + label + ": " + message)

  if label == 'MANUAL_CHECK_S':
    rule.rule_result_mc_s      = message
  elif label == 'MANUAL_CHECK_P':
    rule.rule_result_mc_p      = message
  elif label == 'FAIL_S':
    rule.rule_result_fail_s    = message
  elif label == 'FAIL_P':
    rule.rule_result_fail_p    = message
  elif label == 'HIDDEN_S':
    rule.rule_result_hidden_s  = message
  elif label == 'HIDDEN_P':
    rule.rule_result_hidden_p  = message
  elif label == 'NOT_APPLICABLE':
     rule.rule_result_na       = message
  
  try:   
    rule.save()
  except:
    print("  *** Error saving Rule Result Message: " + label + " : " + message)
      

def addNodeResultMessage(rule, label, message, date):
  print("  Node Result Message: " + label + ": " + message)
  
  if label != "" and message != "": 
    try:   
      nrm = NodeResultMessage(rule=rule, label=label, message=message, updated_date=date)
      nrm.save()
    except:
      print("  *** Error saving Node Result Message: " + label + " : " + message)

# Populate Rule Scope 

try:
  RuleScope.objects.get(rule_scope_code=1)
except ObjectDoesNotExist:  
  rs = RuleScope(rule_scope_code=1, title='Element', abbrev='E', description='Rules apply to the accessibility features of individual elements on a web page')
  rs.save()

try:
  RuleScope.objects.get(rule_scope_code=2)
except ObjectDoesNotExist:  
  rs = RuleScope(rule_scope_code=2, title='Page',    abbrev='P',   description='Rules apply to the accessibility of page layout, structure and identifying the content on the page')
  rs.save()

try:
  RuleScope.objects.get(rule_scope_code=3)
except ObjectDoesNotExist:  
  rs = RuleScope(rule_scope_code=3, title='Website', abbrev='W',   description='Rules apply to the consistency and ordering of content of the web pages within a website, website navigation features and titling that identifies the website and content of indivdiual pages')
  rs.save()

# Populate Rule Group 

title = "Group 1"
desc = 'First set of rules that should be learned and implemented'
try:
  rg = RuleGroup.objects.get(rule_group_code=1)
  rg.title       = title
  rg.description = desc
except ObjectDoesNotExist:  
  rg = RuleGroup(rule_group_code=1, title=title, description=desc)
rg.save()

title = "Group 2"
desc = 'Second set of rules that should be learned and implemented'
try:
  rg = RuleGroup.objects.get(rule_group_code=2)
  rg.title       = title
  rg.description = desc
except ObjectDoesNotExist:  
  rg = RuleGroup(rule_group_code=2, title=title, description=desc)
rg.save()

title = "Group 3"
desc = 'Third (and last) set of rules that should be learned and implemented'
try:
  rg = RuleGroup.objects.get(rule_group_code=4)
  rg.title       = title
  rg.description = desc
except ObjectDoesNotExist:  
  rg = RuleGroup(rule_group_code=4, title=title, description=desc)
rg.save()


for r in data['rules']:
   print("\nRule: " + r['nls_rule_id'])

   resource_properties = ""
   if r['resource_properties'] != "":
     resource_properties = ' '.join(r['resource_properties'])
     print("  Resource Properties: " + resource_properties)

   print("  Getting rule scope: " + str(r['rule_scope']))
   scope = RuleScope.objects.get(rule_scope_code=r['rule_scope'])  

   print("  Getting rule group: " + str(r['rule_group']))
   group = RuleGroup.objects.get(rule_group_code=r['rule_group'])  
     
   try:
     print("  Updating Rule: " + r['nls_rule_id'])
     
     rule = Rule.objects.get(rule_id=r['rule_id'])
     rule.scope=scope
     rule.category = RuleCategory.objects.get(rule_category_code=r['rule_category'])
     rule.group=group
     rule.language_dependancy=r['language_dependency']
     rule.primary_property=r['primary_property']
     rule.resource_properties=resource_properties
     rule.validation=r['validate']
     rule.wcag_primary = WCAG20_SuccessCriterion.get_by_wcag_number(r['wcag_primary'])
     rule.updated_date=r['last_updated']
     
     Technique.objects.filter(rule=rule).delete()  
     ManualCheck.objects.filter(rule=rule).delete()  
     InformationalLink.objects.filter(rule=rule).delete()
     NodeResultMessage.objects.filter(rule=rule).delete()  
     
   except ObjectDoesNotExist:  
     print("  Creating Rule: " + r['nls_rule_id'])
     resource_properties = ",".join(r['resource_properties'])
     rule = Rule(rule_id=r['rule_id'],scope=scope,group=group,language_dependancy=r['language_dependency'],primary_property=r['primary_property'],resource_properties=resource_properties,validation=r['validate'],updated_date=r['last_updated'])
     rule.wcag_primary = WCAG20_SuccessCriterion.get_by_wcag_number(r['wcag_primary'])
     rule.category = RuleCategory.objects.get(rule_category_code=r['rule_category'])
     
   rule.save()

   rule.wcag_related.clear();  
   for related in r['wcag_related']:
      rule.wcag_related.add(WCAG20_SuccessCriterion.get_by_wcag_number(related)) 

   rule.target_resources.clear();  
   for m in r['target_resources']:
     try: 
       rule.target_resources.add(ElementDefinition.get_by_title(m))
     except:
       print("  target resources exception for element definition: " + m  )

   rule.save()

   rule.nls_rule_id    = r['nls_rule_id']
   rule.definition     = r['definition']
   rule.summary        = r['summary']
   
   rule.target_resource_desc = r['target_resource_desc']

   p = r['purpose']

   print("TYPE: " + str(type(p)))

   l = len(p)

   if l > 0:
     rule.purpose_1 = r['purpose'][0]
   else:  
     rule.purpose_1 = ""
     
   if l > 1:
     rule.purpose_2 = r['purpose'][1]
   else:  
     rule.purpose_2 = ""
          
   if l > 2:
     rule.purpose_3 = r['purpose'][2]
   else:  
     rule.purpose_3 = ""
     
   if l > 3:
     rule.purpose_4 = r['purpose'][3]
   else:  
     rule.purpose_4 = ""

   rule.save()
     
   i = 1
   for tech in r['techniques']:
     tech_id = r['rule_id'] + "_T" + str(i)
     i += 1
     addTechnique(rule, tech_id, tech, '', r['last_updated'])

   for mc in r['manual_checks']:
     addManualCheck(rule, mc, '', r['last_updated'])

   informational_links = r['informational_links']
   
   for info in r['informational_links']:
     addInformationalLink(rule, info['type'], info['title'], info['url'], r['last_updated'])

   for message in r['rule_result_messages']:
     addRuleResultMessage(rule, message, r['rule_result_messages'][message], r['last_updated'])

   for message in r['node_result_messages']:
     addNodeResultMessage(rule, message, r['node_result_messages'][message], r['last_updated'])
   
   try:
     rule.save()
   except:
     print("*** Error saving relationships for rule: " + r['nls_rule_id']  )
  