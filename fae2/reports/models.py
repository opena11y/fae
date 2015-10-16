from django.db import models

from django.contrib.auth.models import User

from rulesets.models            import Ruleset



# Create your models here.


class RuleResultsSummary(models.Model):

  page_count         = models.IntegerField(default=0, editable=False)

  rules_violation    = models.IntegerField(default=0, editable=False)
  rules_warning      = models.IntegerField(default=0, editable=False)
  rules_manual_check = models.IntegerField(default=0, editable=False)
  rules_passed       = models.IntegerField(default=0, editable=False)
  rules_na           = models.IntegerField(default=0, editable=False)

  score_violations    = models.IntegerField(default=0, editable=False)
  score_warnings      = models.IntegerField(default=0, editable=False)
  score_manual_checks = models.IntegerField(default=0, editable=False)
  score_passed        = models.IntegerField(default=0, editable=False)

  implementation_score  = models.IntegerField(default=-1, editable=False)
  implementation_status = models.IntegerField(default=-1, editable=False)

  class Meta:
    abstract = True

  def set_rule_results_summary(self, data):
  
    self.page_count         = data.page_count

    self.rules_violation    = data.rules_violation
    self.rules_warning      = data.rules_warning
    self.rules_manual_check = data.rules_manual_check
    self.rules_passed       = data.rules_passed
    self.rules_na           = data.rules_na

    self.score_violations    = data.score_violations
    self.score_warnings      = data.score_warnings
    self.score_manual_checks = data.score_manual_checks
    self.score_passed        = data.score_passed

    self.implementation_score  = data.implementation_score
    self.implementation_status = data.implementation_status 
  
    self.save()

  def calculate_implementation_score(self):
    p    = self.rules_passed
    v_w  = self.rules_violation + self.rules_warning
    
    if p > 0 or v_w > 0: 
      self.implementation_score = (100 * p) / (p + v_w)
    else:
      self.implementation_score = -1
    
    self.implementation_status = 0
  
    if (self.rules_violation > 0) or (self.rules_warning > 0) or (self.rules_passed > 0):
      
      if self.result_score > 99:
        self.implementation_status = 1
      elif self.result_score > 94: 
        self.implementation_status = 2
      elif self.result_score > 49:
        self.implementation_status = 3
      else:
        self.implementation_status = 4
            
    if self.rules_manual_check > 0:
      self.implementation_status += 8

    self.save()  


EVAL_STATUS = (
    ('-', 'Created'),
    ('I', 'Waiting'),
    ('R', 'Initalized'),
    ('P', 'Processing'),
    ('C', 'Saving'),
    ('A', 'Completed'),
    ('E', 'Error'),
)

TYPE_CHOICES = (
    ('rc',    'Rule Category'),
    ('gl',    'WCAG Guideline'),
    ('scope', 'Rule Scope'),
)

VIEW_CHOICES = (
    ('summary',  'Summary Report'),
    ('sitewide', 'Sitewide Report'),
    ('page',     'Page Report'),
)

DEPTH_CHOICES = (
  (1, 'Start URL only'),
  (2, 'First level links'),
  (3, 'Second level links')
)
      
WAIT_TIME_CHOICES = (
  (30000,  ' 30 seconds'),
  (45000,  ' 45 seconds'),
  (60000,  ' 60 seconds'),
  (90000,  ' 90 seconds'),
  (120000, '120 seconds')
)   


# ---------------------------------------------------------------
#
# WebsiteEvaluationResult
#
# ---------------------------------------------------------------

class WebsiteEvaluationReport(RuleResultsSummary):

  id    = models.AutoField(primary_key=True)

  user  = models.ForeignKey(User, editable=True)
    
  slug  = models.SlugField(max_length=256, default="", blank=True, editable=False, unique=True)

  title    = models.CharField("Report Title",  max_length=1024, default="no title")
  
  url      = models.URLField("Start URL",      max_length=1024, default="", blank=True,)
  
  depth    = models.IntegerField("Depth", default=2)
  
  ruleset  = models.ForeignKey(Ruleset)
  
  browser_emulation    = models.CharField("Browser Emulation", max_length=32, default="FIREFOX")

  wait_time            = models.IntegerField("How long to wait for website to load resources (in milliseconds)", choices=WAIT_TIME_CHOICES, default=90000)
  
  span_sub_domains     = models.CharField("Span Sub-Domains (space separated)",    max_length=1024, default="", blank=True)
  exclude_sub_domains  = models.CharField("Exclude Sub-Domains (space separated)", max_length=1024, default="", blank=True)
  
  include_domains      = models.CharField("Include Domains (space separated)",     max_length=1024, default="", blank=True)

  authorization        = models.TextField("Authentication Information",            max_length=8192, default="", blank=True)
  
  # Archiving information

  archive  = models.BooleanField(default=False)
  stats    = models.BooleanField(default=False)
  
  # fae-util and fae20 processing information

  created      = models.DateTimeField(auto_now=False, editable=False)
  last_viewed  = models.DateTimeField(auto_now=True, editable=False)
  status       = models.CharField('Status',  max_length=10, choices=EVAL_STATUS, default='-')  
  
  # processining information    
  processing_time        = models.IntegerField(default=-1)
  processed_urls_count   = models.IntegerField(default=-1)
  unprocessed_urls_count = models.IntegerField(default=-1)
  filtered_urls_count    = models.IntegerField(default=-1)

  data_dir_slug            = models.SlugField(max_length=50, editable=False)
  data_directory           = models.CharField('Data Directory',           max_length=1024, default="")
  data_property_file       = models.CharField('Property File Name',       max_length=1024, default="")
  data_authorization_file  = models.CharField('Authorization File Name',  max_length=1024, default="")
  data_multiple_urls_file  = models.CharField('Multiple URLs File Name',  max_length=1024, default="")
  
  # Rule results summary information


    
  class Meta:
    verbose_name        = "Website Evaluation Report"
    verbose_name_plural = "Website Evaluation Reports"
    ordering = ['created']

  def __unicode__(self):
    return self.title

