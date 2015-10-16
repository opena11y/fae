from django.db import models
from django.contrib.auth.models import User

import re
import CONST
from utilities import OAAMarkupToText, OAAMarkupToHTML
import textile


from markup.models          import ElementDefinition
from ruleCategories.models  import RuleCategory
from wcag20.models          import WCAG20_SuccessCriterion

## Helper class that includes the updated date and creator
class Updated(models.Model):
  updated_date   = models.DateTimeField(auto_now=True, editable=False)
  updated_editor = models.ForeignKey(User, editable=True)




## Rule 
RULE_SCOPE = (
  (0, 'Unknown'), 
  (1, 'Element'),
  (2, 'Page'),
  (3, 'Website'),
)


RULE_SCOPE_HTML_CODE = (
    (0, '<abbr title="Unknown">-</abbr>'),
    (1, '<abbr title="Element">E</abbr>'),
    (2, '<abbr title="Page">P</abbr>'),
    (3, '<abbr title="Website">WS</abbr>'),
)


class RuleScope(models.Model):
  id = models.AutoField(primary_key=True)

  rule_scope_code = models.IntegerField('Scope Code', default=0)
  title           = models.CharField('Scope Title',        max_length=128, default="none")
  abbrev          = models.CharField('Scope Abbreviation', max_length=32,  default="none")
  
  description  = models.CharField('Scope Description', max_length=2048, default="")
  
  class Meta:
    verbose_name        = "Rule Scope"
    verbose_name_plural = "Rule Scopes"
    ordering = ['rule_scope_code',]

  def __str__(self):
      return self.title
      
  def show_scope_html_code(self):
      for shortp, longp in RULE_SCOPE_HTML_CODE:
          if shortp == self.rule_scope_code:
              return longp
              
  def is_element(self):
    return  self.rule_scope_code == 1           

  def is_page(self):
    return  self.rule_scope_code == 2 

  def is_website(self):
    return  self.rule_scope_code == 3          


RULE_GROUP = (
  (0, 'Unknown'), 
  (1, 'Group 1'),
  (2, 'Group 2'),
  (4, 'Group 3'),
)

RULE_GROUP_HTML_CODE = (
  (0, '<abbr title="Unknown">-</abbr>'), 
  (1, '<abbr title="Group 1">1</abbr>'),
  (2, '<abbr title="Group 2">2</abbr>'),
  (4, '<abbr title="Group 3">3</abbr>'),
)

class RuleGroup(models.Model):
  id = models.AutoField(primary_key=True)

  rule_group_code = models.IntegerField('Group Code', default=0)
  title           = models.CharField('Group Title',        max_length=32, default="none")  
  description     = models.CharField('Group Description', max_length=2048, default="")
  
  class Meta:
    verbose_name        = "Rule Group"
    verbose_name_plural = "Rule Groups"
    ordering = ['rule_group_code',]

  def __str__(self):
      return self.title
      
  def show_group_html_code(self):
      for shortp, longp in RULE_GROUP_HTML_CODE:
          if shortp == self.rule_group_code:
              return longp
              



class Rule(models.Model):

  id             = models.AutoField(primary_key=True)
  updated_date   = models.DateTimeField(editable=False)

  rule_id             = models.CharField('Rule ID', max_length=64, unique=True) 
  scope               = models.ForeignKey(RuleScope, related_name='rules')
  group               = models.ForeignKey(RuleGroup, related_name='rules')
  category            = models.ForeignKey(RuleCategory, related_name='rules') 
  wcag_primary        = models.ForeignKey(WCAG20_SuccessCriterion, related_name='rules')
  wcag_related        = models.ManyToManyField(WCAG20_SuccessCriterion, related_name='related_rules')  
  target_resources    = models.ManyToManyField(ElementDefinition, related_name='rules') 
  primary_property    = models.CharField('primary attribute or property used by the rule', max_length=64, default='')
  resource_properties = models.CharField('Comma separated list of cache properties and attributes used by the rule', max_length=250)
  language_dependancy = models.CharField('Language codes separated by commas', max_length=100, default='')
  validation          = models.TextField('Javascript code for validation function', null=True,blank=True)

  nls_rule_id     = models.CharField('Translated Rule ID', max_length=64) 
  
  definition      = models.CharField('Rule Definition', max_length=512)
  definition_html = models.CharField(max_length=512, default="")
  summary         = models.CharField('Rule Summary (shorter version of definition)', max_length=128)
  summary_html    = models.CharField(max_length=256, default="")
  summary_text    = models.CharField(max_length=128, default="")
  
  target_resource_desc      = models.CharField('Summary of the types of element definitions this rule tests', max_length=512)
  target_resource_desc_html = models.CharField(max_length=512)
  
  purpose_1      = models.CharField('Purpose 1 (i.e how does the rule help people with disabilites)', max_length=512)
  purpose_1_html = models.CharField(max_length=512, default="")
  purpose_2      = models.CharField('Purpose 2', null=True, blank=True, max_length=512)
  purpose_2_html = models.CharField(max_length=512, default="")
  purpose_3      = models.CharField('Purpose 3', null=True, blank=True, max_length=512)
  purpose_3_html = models.CharField(max_length=512, default="")
  purpose_4      = models.CharField('Purpose 4', null=True, blank=True, max_length=512)
  purpose_4_html = models.CharField(max_length=512, default="")
  
  rule_result_mc_s     = models.CharField('Rule Result Message: One manual check'            , null=True, blank=True, max_length=512)
  rule_result_mc_p     = models.CharField('Rule Result Message: More than one manual check'  , null=True, blank=True, max_length=512)
  rule_result_fail_s   = models.CharField('Rule Result Message: One failed element'          , null=True, blank=True, max_length=512)
  rule_result_fail_p   = models.CharField('Rule Result Message: More than one failed element', null=True, blank=True, max_length=512)
  rule_result_hidden_s = models.CharField('Rule Result Message: One hidden element'          , null=True, blank=True, max_length=512)
  rule_result_hidden_p = models.CharField('Rule Result Message: More than one hidden element', null=True, blank=True, max_length=512)
  rule_result_na       = models.CharField('Rule Result Message: Not Applicable Message'      , null=True, blank=True, max_length=512)
    
  class Meta:
    verbose_name        = "Rule"
    verbose_name_plural = "Rules"
    ordering = ['nls_rule_id',]
    unique_together = (('rule_id', 'definition'),)

  def __str__(self):
      return self.nls_rule_id

  def save(self):
    self.definition_html              = OAAMarkupToHTML(self.definition)
    self.summary_html                 = OAAMarkupToHTML(self.summary)
    self.summary_text                 = OAAMarkupToText(self.summary)
    if self.target_resource_desc:
      self.target_resource_desc_html    = OAAMarkupToHTML(self.target_resource_desc)
    if self.purpose_1:
      self.purpose_1_html               = OAAMarkupToHTML(self.purpose_1)
    if self.purpose_2:
      self.purpose_2_html               = OAAMarkupToHTML(self.purpose_2)
    if self.purpose_2:
      self.purpose_3_html               = OAAMarkupToHTML(self.purpose_3)
    if self.purpose_2:
      self.purpose_4_html               = OAAMarkupToHTML(self.purpose_4)
    super(Rule, self).save() # Call the "real" save() method.

  def get_scope(self):
    for shortp, longp in RULE_SCOPE:
      if shortp == self.scope:
         return longp

  def show_scope(self):
    return self.get_scope()
  
  def get_wcag_primary(self):
    return "%s %s (Level %s)"%(self.wcag_primary.number(), self.wcag_primary.title, self.wcag_primary.show_level_html_code())
   
  def wcag20_requirements(self):
    return "%s - %s"%(self.wcag_primary.number(),self.wcag_related_list())

  def get_previous_rule_by_wcag_success_criteria(self):
    rules = Rule.objects.order_by('wcag_primary','category',)
    pr = 0
    for r in rules:
      if r == self:
        return pr
      else: 
        pr = r
   
    return pr

  def natural_key(self):
      return (self.rule_id, self.definition, self.summary, self.purpose_1, self.purpose_2, self.purpose_3, self.purpose_4)

  def basic_mapping(self):
      rm = self.rule_mappings.get(ruleset__ruleset_id='BASIC')
      if rm:
        if rm.required:
          return 2
        else:
          return 1  
      return 0

  def aria_trans_mapping(self):
      rm = self.rule_mappings.get(ruleset__ruleset_id='ARIA_TRANS')
      if rm:
        if rm.required:
          return 2
        else:
          return 1  
      return 0

  def definition_text(self):  
    return OAAMarkupToText(self.definition)

  def aria_strict_mapping(self):
      rm = self.rule_mappings.get(ruleset__ruleset_id='ARIA_STRICT')
      if rm:
        if rm.required:
          return 2
        else:
          return 1  
      return 0


## Information link
NODE_RESULT_LABEL_CHOICES = (
    ('ELEMENT_PASS_1',   'ELEMENT_PASS_1'),
    ('ELEMENT_PASS_2',   'ELEMENT_PASS_2'),
    ('ELEMENT_PASS_3',   'ELEMENT_PASS_3'),
    ('ELEMENT_PASS_4',   'ELEMENT_PASS_4'),
    ('ELEMENT_PASS_5',   'ELEMENT_PASS_5'),
    ('ELEMENT_FAIL_1',   'ELEMENT_FAIL_1'),
    ('ELEMENT_FAIL_2',   'ELEMENT_FAIL_2'),
    ('ELEMENT_FAIL_3',   'ELEMENT_FAIL_3'),
    ('ELEMENT_FAIL_4',   'ELEMENT_FAIL_4'),
    ('ELEMENT_FAIL_5',   'ELEMENT_FAIL_5'),
    ('ELEMENT_MC_1',     'ELEMENT_MC_1'),
    ('ELEMENT_MC_2',     'ELEMENT_MC_2'),
    ('ELEMENT_MC_3',     'ELEMENT_MC_3'),
    ('ELEMENT_MC_4',     'ELEMENT_MC_4'),
    ('ELEMENT_MC_5',     'ELEMENT_MC_5'),
    ('ELEMENT_HIDDEN_1', 'ELEMENT_HIDDEN_1'),
    ('ELEMENT_HIDDEN_2', 'ELEMENT_HIDDEN_2'),
    ('PAGE_PASS_1', 'PAGE_PASS_1'),
    ('PAGE_PASS_2', 'PAGE_PASS_2'),
    ('PAGE_PASS_3', 'PAGE_PASS_3'),
    ('PAGE_PASS_4', 'PAGE_PASS_4'),
    ('PAGE_PASS_5', 'PAGE_PASS_5'),
    ('PAGE_FAIL_1', 'PAGE_FAIL_1'),
    ('PAGE_FAIL_2', 'PAGE_FAIL_2'),
    ('PAGE_FAIL_3', 'PAGE_FAIL_3'),
    ('PAGE_FAIL_4', 'PAGE_FAIL_4'),
    ('PAGE_FAIL_5', 'PAGE_FAIL_5'),
    ('PAGE_MC_1',   'PAGE_MC_1'),
    ('PAGE_MC_2',   'PAGE_MC_2'),
    ('PAGE_MC_3',   'PAGE_MC_3'),
    ('PAGE_MC_4',   'PAGE_MC_4'),
    ('PAGE_MC_5',   'PAGE_MC_5'),
    ('WEBSITE_PASS_1', 'WEBSITE_PASS_1'),
    ('WEBSITE_PASS_2', 'WEBSITE_PASS_2'),
    ('WEBSITE_PASS_3', 'WEBSITE_PASS_3'),
    ('WEBSITE_PASS_4', 'WEBSITE_PASS_4'),
    ('WEBSITE_PASS_5', 'WEBSITE_PASS_5'),
    ('WEBSITE_FAIL_1', 'WEBSITE_FAIL_1'),
    ('WEBSITE_FAIL_2', 'WEBSITE_FAIL_2'),
    ('WEBSITE_FAIL_3', 'WEBSITE_FAIL_3'),
    ('WEBSITE_FAIL_4', 'WEBSITE_FAIL_4'),
    ('WEBSITE_FAIL_5', 'WEBSITE_FAIL_5'),
    ('WEBSITE_MC_1',   'WEBSITE_MC_1'),
    ('WEBSITE_MC_2',   'WEBSITE_MC_2'),
    ('WEBSITE_MC_3',   'WEBSITE_MC_3'),
    ('WEBSITE_MC_4',   'WEBSITE_MC_4'),
    ('WEBSITE_MC_5',   'WEBSITE_MC_5'),
)

class NodeResultMessage(models.Model):
  id = models.AutoField(primary_key=True)
  
  updated_date   = models.DateTimeField(editable=False)
  
  rule         = models.ForeignKey(Rule, related_name="node_result_messages")
  label        = models.CharField('Label',  choices=NODE_RESULT_LABEL_CHOICES, max_length=32)
  message      = models.CharField('Message', max_length=512)

  class Meta:
        ordering = ['label',]
        verbose_name="Node Result Message"
        verbose_name_plural="Node Result Message"



## Information link
INFORMATIONAL_LINK_TYPE = (
    ('0', 'Unknown'),
    ('1', 'W3C Specification'),
    ('2', 'WCAG 2.0 Technique'),
    ('3', 'Technique'),
    ('4', 'Example'),
    ('5', 'Manual Check Proceedure'),
    ('6', 'Authoring Tool'),
    ('7', 'Code Library or Product Documentation'),
    ('8', 'Other Resource'),
)


class InformationalLink(models.Model):
  id = models.AutoField(primary_key=True)
  
  updated_date   = models.DateTimeField(editable=False)

  rule         = models.ForeignKey(Rule, related_name="informational_links")
  title        = models.CharField('Information Link Title', max_length=512)
  title_html   = models.CharField(max_length=512)
  type         = models.CharField('Type of Information Link',choices=INFORMATIONAL_LINK_TYPE, default='0', max_length=8)  
  url          = models.URLField('Information Link URL', max_length=512);

  class Meta:
        ordering = ['rule', 'title', 'type', 'url']
        verbose_name="Informational Link"
        verbose_name_plural="Informational Links"

  def save(self):
    self.title_html = OAAMarkupToHTML(self.title)
    super(InformationalLink, self).save() # Call the "real" save() method.
