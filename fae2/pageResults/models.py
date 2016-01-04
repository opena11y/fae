from django.db import models

from reports.models        import WebsiteReport
from ruleCategories.models import RuleCategory
from wcag20.models         import Guideline
from rules.models          import RuleScope
from rules.models          import Rule

from reports.models import IMPLEMENTATION_STATUS_CHOICES

from websiteResults.models import RuleResult
from websiteResults.models import RuleGroupResult
from websiteResults.models import WebsiteRuleCategoryResult
from websiteResults.models import WebsiteGuidelineResult
from websiteResults.models import WebsiteRuleScopeResult
from websiteResults.models import WebsiteRuleResult

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
    ordering = ['page_number']

  def __str__(self):
    return self.url

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

  slug            = models.SlugField(max_length=32, default="none", blank=True, editable=False)

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

  slug            = models.SlugField(max_length=32, default="none", blank=True, editable=False)

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

  slug            = models.SlugField(max_length=32, default="none", blank=True, editable=False)

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

  slug            = models.SlugField(max_length=32, default="none", blank=True, editable=False)
  
  ws_rule_result  = models.ForeignKey(WebsiteRuleResult,      related_name="page_rule_results", blank=True)

  page_result     = models.ForeignKey(PageResult,             related_name="page_rule_results")
  page_rc_result  = models.ForeignKey(PageRuleCategoryResult, related_name="page_rule_results")
  page_gl_result  = models.ForeignKey(PageGuidelineResult,    related_name="page_rule_results")
  page_rs_result  = models.ForeignKey(PageRuleScopeResult,    related_name="page_rule_results")

  result_message  = models.CharField("Rule Result Message", max_length=4096, default="none")

  elements_passed        = models.IntegerField(default=0)
  elements_violation     = models.IntegerField(default=0)
  elements_warning       = models.IntegerField(default=0)
  elements_hidden        = models.IntegerField(default=0)

  elements_mc_identified  = models.IntegerField(default=0)
  elements_mc_passed      = models.IntegerField(default=0)
  elements_mc_failed      = models.IntegerField(default=0)
  elements_mc_na          = models.IntegerField(default=0)

  element_results_json   = models.TextField(default="", blank=True)

  class Meta:
    verbose_name        = "Page Rule Result"
    verbose_name_plural = "Page Rule Results"
    ordering = ['-elements_violation', '-elements_warning', '-elements_mc_identified', '-elements_passed', '-elements_hidden' ]

  def calculate_implementation(self):
    self.implementation_pass_fail_score  = -1  
    self.implementation_score       = -1  
    self.implementation_status      = "U"  

#    debug('V: ' + str(self.elements_violation) + ' W: ' + str(self.elements_warning) + ' MC: ' + str(self.elements_manual_check) + ' P: ' + str(self.elements_passed))

    total_pass_fail = self.elements_violation + self.elements_warning + self.elements_passed + self.elements_mc_passed + self.elements_mc_failed
    total = self.elements_mc_identified - self.elements_mc_passed - self.elements_mc_failed - self.elements_mc_na
    if total > 0:
      total = total_pass_fail + total
    else:
      total = total_pass_fail
      

#    debug('TOTAL: ' + str(total))

    passed = self.elements_passed+self.elements_mc_passed

    if total:
      self.implementation_pass_fail_score  =  (100 * passed) / total_pass_fail
      self.implementation_score            =  (100 * passed) / total
      self.implementation_status = "NI"  
      if self.implementation_score > 50:
        self.implementation_status = "PI"  
      if self.implementation_score > 95:
        self.implementation_status = "AC"  
      if self.elements_passed == total:
        self.implementation_status = "C"  
    else:
      self.implementation_status = "NA"  

    self.save()  


  def __str__(self):
    return "Page Rule Result: " + self.result_message


  def get_id(self):
    return 'prr_' + self.id   



