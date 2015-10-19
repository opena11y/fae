from django.db import models

# Ruleset models

import utils.CONST
from utils.utilities import OAAMarkupToHTML, OAAMarkupToText
import textile


from ruleCategories.models import RuleCategory

## Rule Sets (e.g. WCAG20_ARIA_STRICT)
class Ruleset(models.Model):
  id             = models.AutoField(primary_key=True)
  updated_date   = models.DateTimeField(editable=False)
  
  ruleset_id         = models.CharField(max_length=64) 
  version            = models.CharField('Ruleset Version', max_length=16, default="unknown")
  slug               = models.SlugField(max_length=64, null=True,blank=True)
  title              = models.CharField('Ruleset Title', max_length=128)
  title_html         = models.CharField(max_length=512, default="")
  title_text         = models.CharField(max_length=128, default="")
  tooltip            = models.CharField(max_length=512,  default="")
  tooltip_html       = models.CharField(max_length=2014,  default="")
  tooltip_text       = models.CharField(max_length=512,  default="")
  web_resources      = models.TextField('Target Web Resources', default="")
  web_resources_html = models.TextField(default="", null=True,blank=True)
  description        = models.TextField(null=True,blank=True)
  description_html   = models.TextField(blank=True, default="")
  author             = models.CharField('Ruleset Author',max_length=64, default="unknown")
  author_url         = models.URLField('Ruleset Author URL',max_length=256, default="")

  class Meta:
    verbose_name        = "Ruleset"
    verbose_name_plural = "Rulesets"
    ordering = ['title_text']
    
  def __str__(self):
      return self.title_text 

  def save(self):
    if not self.slug:
      self.slug = self.ruleset_id
      
    self.title_html = OAAMarkupToHTML(self.title)
    self.title_text = OAAMarkupToText(self.title)
    
    self.tooltip_html = OAAMarkupToHTML(self.tooltip)
    self.tooltip_text = OAAMarkupToText(self.tooltip)
    
    if self.web_resources:
      self.web_resources_html = textile.textile(self.web_resources)
      
    if self.description:   
      self.description_html  = textile.textile(self.description)
      
    super(Ruleset, self).save() # Call the "real" save() method.  
    
  @models.permalink
  def get_show_ruleset_url(self):
    return ('ruleset', [self.slug, 'rc'])     
    
  def get_number_of_rules(self):
    return len(self.rule_mappings.all())

  def get_number_of_required_rules(self):
    count = 0
    for rm in self.rule_mappings.all():
      if rm.required:
        count += 1
      
    return count

  def get_number_of_recommended_rules(self):
    count = 0
    for rm in self.rule_mappings.all():
      if not rm.required:
        count += 1
    return count


  def get_rule_type(self, rule):
    for rm in self.rule_mappings.all():
      if rm.rule == rule:
        return rm.required
    
    return False

  def get_rules_by_rule_categories(self):

    class RuleCategoryItem(object):

      def __init__(self, rc):
        self.rule_category = rc
        self.rule_mappings = []


    rcs = []

    rule_categories = RuleCategory.objects.all()

    for rc in rule_categories:

      rc_item = RuleCategoryItem(rc)

      for rm in self.rule_mappings.all():
        if rm.rule.category == rc:
          rc_item.rule_mappings.append(rm)

      rcs.append(rc_item)

    return rcs  


  def get_rules_by_wcag(self):

    class GuidelineItem(object):

      def __init__(self, g):
        self.guideline = g
        self.success_criteria = []


    class SuccessCriteriaItem(object):

      def __init__(self, sc):
        self.success_criterion = sc
        self.rule_mappings = []


    gs = []

    guidelines = WCAG20_Guideline.objects.all()

    for g in guidelines:

      g_item = GuidelineItem(g)

      for sc in g.success_criteria.all():

        sc_item = GuidelineItem(g)

        for rm in self.rule_mappings.all():
          if rm.wcag_primary == sc:
            sc_item.rule_mappings.append(rm)

        g_item.success_criteria.append(sc_item)

      gs.append(g_item)

    return gs  




