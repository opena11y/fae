from django.db import models

from reports.models import WebsiteReport
from ruleCategories.models import RuleCategory
from wcag20.models         import Guideline
from rules.models          import RuleScope
from rules.models          import Rule

# Create your models here.


IMPLEMENTATION_STATUS_CHOICES = (
    ('U',   'Undefined'),
    ('NA',  'Not applicable'),
    ('NI',  'Not Implemented'),
    ('PI',  'Partial Implementation'),
    ('AC',  'Almost Complete'),
    ('C',   'Complete'),
)


MC_STATUS_CHOICES = (
    ('NC',  'Not Checked'),
    ('NA',  'Not Applicable'),
    ('P',   'Passed'),
    ('F',   'Fail'),
)

# ---------------------------------------------------------------
#
# RuleResult
#
# ---------------------------------------------------------------

class RuleResult(models.Model):
  result_value           = models.IntegerField(default=0)

  implementation_pass_fail_score  = models.IntegerField(default=-1)
  implementation_score            = models.IntegerField(default=-1)

  implementation_pass_fail_status  = models.CharField("Implementation Pass/Fail Status",  max_length=2, choices=IMPLEMENTATION_STATUS_CHOICES, default='U')
  implementation_status            = models.CharField("Implementation Status",  max_length=2, choices=IMPLEMENTATION_STATUS_CHOICES, default='U')

  manual_check_status    = models.CharField("Manual Check Status",  max_length=2, choices=MC_STATUS_CHOICES, default='NC')

  class Meta:
        abstract = True




# ---------------------------------------------------------------
#
# RuleGroupResult
#
# ---------------------------------------------------------------

class RuleGroupResult(RuleResult):
  rules_violation    = models.IntegerField(default=0)
  rules_warning      = models.IntegerField(default=0)
  rules_manual_check = models.IntegerField(default=0)
  rules_passed       = models.IntegerField(default=0)
  rules_na           = models.IntegerField(default=0)

  rules_with_hidden_content = models.IntegerField(default=0)

  class Meta:
        abstract = True


# ---------------------------------------------------------------
#
# WebsiteAllRulesResult
#
# ---------------------------------------------------------------

class WebsiteResult(RuleGroupResult):
  id                 = models.AutoField(primary_key=True)

  ws_report          = models.ForeignKey(WebsiteReport, related_name="ws_all_results")

  class Meta:
    verbose_name        = "Website Result"
    verbose_name_plural = "Website Results"

  def __str__(self):
    return "Website Results"

  def get_id(self):
    return 'wsr' + self.id   


# ---------------------------------------------------------------
#
# WebsiteRuleCategoryResult
#
# ---------------------------------------------------------------

class WebsiteRuleCategoryResult(RuleGroupResult):
  id                  = models.AutoField(primary_key=True)

  ws_report           = models.ForeignKey(WebsiteReport, related_name="ws_rc_results")

  rule_category       = models.ForeignKey(RuleCategory)

  verbose_name        = "Website Rule Category Result"
  verbose_name_plural = "Website Rule Category Results"
  ordering            = ['rule_category']

  def __unicode__(self):
    return self.rule_category.title_plural 

  def get_title(self):
    return self.rule_category.title   

  def get_id(self):
    return 'wsrcr_' + self.rule_category.id   


# ---------------------------------------------------------------
#
# WebsiteGuidelineResult
#
# ---------------------------------------------------------------    

class WebsiteGuidelineResult(RuleGroupResult):
  id                 = models.AutoField(primary_key=True)

  ws_report           = models.ForeignKey(WebsiteReport, related_name="ws_gl_results")

  guideline            = models.ForeignKey(Guideline)

  class Meta:
    verbose_name        = "Website Guideline Result"
    verbose_name_plural = "Website Guideline Results"
    ordering = ['guideline']

  def __unicode__(self):
    return str(self.guideline) 

  def get_group_title(self):
    return self.guideline.title   

  def get_group_id(self):
    return 'wsglr_' + self.guideline.id   

# ---------------------------------------------------------------
#
# WebsiteRuleScopeResult
#
# ---------------------------------------------------------------

class WebsiteRuleScopeResult(RuleGroupResult):
  id               = models.AutoField(primary_key=True)

  ws_report        = models.ForeignKey(WebsiteReport, related_name="ws_rs_results")

  rule_scope       = models.ForeignKey(RuleScope)  


  class Meta:
    verbose_name        = "Website Rule Scope Result"
    verbose_name_plural = "Website Rule Scope Results"
    ordering = ['-rule_scope']

  def __unicode__(self):
    return self.rule_scope.title 
    
  def get_title(self):
    return self.rule_scope.title   

  def get_id(self):
    return 'wsrsr_' + self.rule_scope.id   


# ---------------------------------------------------------------
#
# WebsiteRuleResult
#
# ---------------------------------------------------------------

class WebsiteRuleResult(RuleResult):
  id                 = models.AutoField(primary_key=True)

  rule                  = models.ForeignKey(Rule)
  rule_required         = models.BooleanField(default=False)
  
  ws_result     = models.ForeignKey(WebsiteResult,              related_name="ws_rule_results")
  
  ws_rc_result  = models.ForeignKey(WebsiteRuleCategoryResult,  related_name="ws_rule_results")
  ws_gl_result  = models.ForeignKey(WebsiteGuidelineResult,     related_name="ws_rule_results")
  ws_rs_result  = models.ForeignKey(WebsiteRuleScopeResult,     related_name="ws_rule_results")

  rule_number   = models.IntegerField(default=-1)

  pages_violation    = models.IntegerField(default=0)
  pages_warning      = models.IntegerField(default=0)
  pages_manual_check = models.IntegerField(default=0)
  pages_passed       = models.IntegerField(default=0)
  pages_na           = models.IntegerField(default=0)

  pages_with_hidden_content  = models.IntegerField(default=0)

  class Meta:
    verbose_name        = "Website Rule Result"
    verbose_name_plural = "Website Rule Results"
    ordering = ['-pages_violation', '-pages_warning', '-pages_manual_check', '-pages_passed', '-pages_with_hidden_content', '-rule__scope']

  def __unicode__(self):
    return "Website Rule Result: " + self.rule.summary_text 

  def get_id(self):
    return 'wsrr_' + self.rule.id  
    
       
