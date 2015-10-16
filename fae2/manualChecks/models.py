from django.db import models
from django.contrib.auth.models import User
import re

from django.core import urlresolvers

# Create your models here.

import CONST
from utilities import OAAMarkupToHTML, OAAMarkupToText 
import textile


from rules.models import Rule, Updated

## Manual check of rule
class ManualCheck(models.Model):
  id             = models.AutoField(primary_key=True)
  updated_date   = models.DateTimeField(editable=False)
  
  rule        = models.ForeignKey(Rule, related_name="manual_checks")
  title       = models.CharField('Manual Check Title',      max_length=512)
  title_html  = models.CharField(max_length=512)
  description = models.TextField('Manual Check Description', null=True,blank=True)
  description_html = models.TextField(null=True,blank=True)
  url         = models.URLField('Manual Check URL',   null=True, blank=True)

  class Meta:
    verbose_name        = "Manual Check"
    verbose_name_plural = "Manual Checks"
    ordering = ['rule', 'title']


  def __str__(self):
    return "Manual Checks: " + str(self.rule)

  def save(self):
    if self.title:
      self.title_html = OAAMarkupToHTML(self.title)
      
    if self.description:
      self.description_html  = textile.textile(self.description)
      
    super(ManualCheck, self).save() # Call the "real" save() method.  

  def get_admin_url(self):
    return urlresolvers.reverse('admin:manualChecks_manualcheck_change', args=(self.id,)) 



