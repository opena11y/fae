from django.db import models
from django.contrib.auth.models import User
import re

from django.core import urlresolvers

# Create your models here.

import utils.CONST
from utils.utilities import OAAMarkupToHTML, OAAMarkupToText
import textile


from rules.models import Rule, Updated

TECHNIQUE_TYPE = (
  ('PR', 'Preferred technique, should be used whenever possible'),
  ('SP', 'Special case, should only be used when preferred techniques are not possible'),
)

class Technique(models.Model):
  id             = models.AutoField(primary_key=True)
  updated_date   = models.DateTimeField(editable=False)

  technique_id =  models.CharField('Technique ID', max_length=64, unique=True) 
  rule         = models.ForeignKey(Rule, related_name="techniques")
  type         = models.CharField('Technique Type',  max_length=2,   choices=TECHNIQUE_TYPE, default='PR')
  title        = models.CharField('Technique Title', max_length=512)
  title_html   = models.CharField(max_length=1024, default="")
  abbrev       = models.CharField('Technique Abbreviation', max_length=128, null=True,blank=True )
  abbrev_html  = models.CharField(max_length=256, default="")
  notes        = models.TextField('Technique Notes', null=True,blank=True)
  notes_html   = models.TextField(default="")
  url          = models.URLField('Technique URL', null=True, blank=True)
  
  class Meta:
    verbose_name        = "Technique"
    verbose_name_plural = "Techniques"
    ordering = ['rule', 'type']
  
  def save(self):
    if self.title:
      self.title_html = OAAMarkupToHTML(self.title)
    if self.abbrev:
      self.abbrev_html = OAAMarkupToHTML(self.abbrev)
    if self.notes:
      self.notes_html  = textile.textile(self.notes)
    super(Technique, self).save() # Call the "real" save() method.
    
  def __str__(self):
      return str(self.rule.nls_rule_id) + ': ' + self.title 
      
  def get_admin_url(self):
    return urlresolvers.reverse('admin:techniques_technique_change', args=(self.id,))
  


