import sys,os
import django
from django.core.exceptions import ObjectDoesNotExist

sys.path.append(os.path.abspath('..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fae2.settings')
from django.conf import settings

django.setup()

import json

"""This file is for populating the database with markup information
I empty it. Run as a standalone script!"""

from django.core.exceptions import ObjectDoesNotExist
from rulesets.models import Ruleset, RuleMapping
from rules.models import Rule

from django.contrib.auth.models import User

json_data=open('oaa_exported_rules.json')

data = json.load(json_data)

json_data.close()

u = User.objects.all()[0]

RuleMapping.objects.all().delete()

def create_ruleset(ruleset_id, version, title, tooltip, desc, author, author_url, date, editor):
  try:
    ruleset = Ruleset.objects.get(ruleset_id=ruleset_id)
    print("  Updating Ruleset: " + ruleset_id)
    ruleset.version        = version
    ruleset.title          = title
    ruleset.tooltip        = tooltip
    ruleset.description    = desc
    ruleset.author         = author
    ruleset.author_url     = author_url
    ruleset.updated_date   = date
    ruleset.updated_editor = editor
  except ObjectDoesNotExist:
    print("  Creating Ruleset: " + title )
    ruleset = Ruleset(ruleset_id=ruleset_id, version=version, title=title, tooltip=tooltip, description=desc, author=author, author_url=author_url, updated_date=date)
  ruleset.save()
  return ruleset
    
  
def create_rule_mapping(ruleset, rule_id, required, enabled):
  try:
    rule = Rule.objects.get(rule_id=rule_id)
    print("  " + ruleset.ruleset_id + " " + rule.nls_rule_id + " " + str(required) + " " + str(enabled))
    
    try:
      rm = RuleMapping.objects.get(ruleset=ruleset, rule=rule)
      print("  Updating Rule Mapping for " + ruleset.ruleset_id + " and rule " + rule.nls_rule_id)
      rm.required = required
      rm.enabled  = enabled
    except ObjectDoesNotExist:
      print("  Creating Rule Mapping for " + ruleset.ruleset_id + " and rule " + rule.nls_rule_id)
      rm = RuleMapping(ruleset=ruleset, rule=rule, required=required, enabled=enabled)
    rm.save()
    return rm
  except ObjectDoesNotExist:
    print("  Could not find rule with id: " + rule_id)
    return null

for rs in data['rulesets']:
   print("\nRuleset: " + rs['ruleset_id'])
   
   rs2 = create_ruleset(rs['ruleset_id'], rs['ruleset_version'], rs['ruleset_title'], rs['ruleset_tooltip'], rs['ruleset_description'], rs['ruleset_author_name'], rs['ruleset_author_url'], rs['ruleset_updated'], u)
   
   for rm in rs['rule_mappings']:
       print("\n    " + rm)
       create_rule_mapping(rs2, rm, rs['rule_mappings'][rm]['required'], rs['rule_mappings'][rm]['enabled'])
      
