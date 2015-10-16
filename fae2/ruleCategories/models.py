from django.db import models
from django.contrib.auth.models import User
import re

# Rule Category models

import utils.CONST

## Rule Categories (e.g. abbrev, audio, headings, images, links...)  
class RuleCategory(models.Model):
  id = models.AutoField(primary_key=True)
  
  rule_category_code  = models.IntegerField(unique=True)
  category_id         = models.CharField(max_length=64) 
  title               = models.CharField(max_length=256)
  title_plural        = models.CharField("Title Plural", max_length=256)
  description         = models.TextField(null=True,blank=True)
  slug                = models.SlugField(max_length=32)
  order               = models.IntegerField()

  class Meta:
    verbose_name        = "Rule Category"
    verbose_name_plural = "Rule Categories"
    ordering = ['order','title']
    
  def __str__(self):
    return self.title_plural

  def natural_key(self):
    return (self.id, self.rule_category_code, self.category_id, self.title, self.description)

  def get_rules(self):

    rules = []
    
    for r in self.rules.all():
      rules.append(r)

    return rules



