from django.db import models

from reports.models        import WebsiteReport
from ruleCategories.models import RuleCategory
from wcag20.models         import Guideline
from rules.models          import RuleScope
from rules.models          import Rule


from websiteResults.models import IMPLEMENTATION_STATUS_CHOICES
from websiteResults.models import RuleResult
from websiteResults.models import RuleGroupResult
from websiteResults.models import WebsiteResult
from websiteResults.models import WebsiteRuleCategoryResult
from websiteResults.models import WebsiteGuidelineResult
from websiteResults.models import WebsiteRuleScopeResult

# Create your models here.

# ---------------------------------------------------------------
#
# PageResult
#
# ---------------------------------------------------------------

class PageResult(RuleGroupResult):
  id                 = models.AutoField(primary_key=True)

  ws_report        = models.ForeignKey(WebsiteReport, related_name="page_all_results")

  # Page identification information
  
  page_number   = models.IntegerField(default=-1)

  url            = models.URLField( 'Page URL',           max_length=4096, default="")
  url_encoded    = models.URLField( 'Page URL (encoded)', max_length=8192, default="")
  title          = models.CharField('Page Title',         max_length=512, default="")

  class Meta:
    verbose_name        = "Page Result"
    verbose_name_plural = "Page Results"

  def __str__(self):
    return "Page Result"

  def get_title(self):
    return "Page Result: " + self.title   

  def get_id(self):
    return 'pr_' + self.id   


# ---------------------------------------------------------------
#
# PageRuleCategoryResult
#
# ---------------------------------------------------------------

class PageRuleCategoryResult(RuleGroupResult):
  id              = models.AutoField(primary_key=True)

  page_result     = models.ForeignKey(PageResult, related_name="page_rc_results")

  ws_rc_result    = models.ForeignKey(WebsiteRuleCategoryResult, related_name="page_rc_results", blank=True, null=True)

  rule_category   = models.ForeignKey(RuleCategory)

  class Meta:
    verbose_name        = "Page Rule Category Result"
    verbose_name_plural = "Page Rule Category Results"
    ordering            = ['rule_category']

  def __str__(self):
    return self.rule_category.title

  def get_title(self):
    return self.rule_category.title

  def get_id(self):
    return 'prcr_' + self.id   


# ---------------------------------------------------------------
#
# PageGuidelineResult
#
# ---------------------------------------------------------------    

class PageGuidelineResult(RuleGroupResult):
  id                 = models.AutoField(primary_key=True)

  page_result   = models.ForeignKey(PageResult, related_name="page_gl_results")

  ws_gl_result  = models.ForeignKey(WebsiteGuidelineResult, related_name="page_gl_results", blank=True, null=True)

  guideline     = models.ForeignKey(Guideline)

  class Meta:
    verbose_name        = "Page Guideline Result"
    verbose_name_plural = "Page Guideline Results"
    ordering = ['guideline']

  def __str__(self):
    return str(self.guideline) 

  def get_title(self):
    return self.guideline.title   

  def get_id(self):
    return 'pglr_' + self.id

# ---------------------------------------------------------------
#
# PageRuleScopeResult
#
# ---------------------------------------------------------------

class PageRuleScopeResult(RuleGroupResult):
  id            = models.AutoField(primary_key=True)

  page_result   = models.ForeignKey(PageResult, related_name="page_rs_results")

  ws_rs_result  = models.ForeignKey(WebsiteRuleScopeResult, related_name="page_rs_results", blank=True, null=True)

  rule_scope    = models.ForeignKey(RuleScope)  


  class Meta:
    verbose_name        = "Page Rule Scope Result"
    verbose_name_plural = "Page Rule Scope Results"
    ordering = ['-rule_scope']

  def __str__(self):
    return self.rule_scope.title 
    
  def get_title(self):
    return self.rule_scope.title   

  def get_id(self):
    return 'prsr_' + self.id   



# ---------------------------------------------------------------
#
# PageRuleResult
#
# ---------------------------------------------------------------

class PageRuleResult(RuleResult):
  id          = models.AutoField(primary_key=True)

  rule           = models.ForeignKey(Rule)
  rule_required  = models.BooleanField(default=False)
  
  page_result     = models.ForeignKey(PageResult,             related_name="page_rule_results")
  page_rc_result  = models.ForeignKey(PageRuleCategoryResult, related_name="page_rule_results")
  page_gl_result  = models.ForeignKey(PageGuidelineResult,    related_name="page_rule_results")
  page_rs_result  = models.ForeignKey(PageRuleScopeResult,    related_name="page_rule_results")

  message                = models.CharField("Rule Result Message", max_length=4096, default="none")

  elements_passed        = models.IntegerField(default=0)
  elements_violation     = models.IntegerField(default=0)
  elements_warning       = models.IntegerField(default=0)
  elements_manual_check  = models.IntegerField(default=0)
  elements_hidden        = models.IntegerField(default=0)

  element_results_json   = models.TextField(default="", blank=True)

  class Meta:
    verbose_name        = "Page Rule Result"
    verbose_name_plural = "Page Rule Results"
    ordering = ['-elements_violation', '-elements_warning', '-elements_manual_check', '-elements_passed', '-elements_hidden' ]

  def __str__(self):
    return "Page Rule Result: " + self.message

  def get_title(self):
    return self.rule.summary_text   

  def get_id(self):
    return 'prr_' + self.id   



