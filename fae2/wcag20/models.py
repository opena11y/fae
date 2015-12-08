from django.db import models

# Create your models here.

## WCAG Principal
class Principle(models.Model):
  id      = models.AutoField(primary_key=True)

  title   = models.CharField(max_length=200)
  num     = models.IntegerField()
  number  = models.CharField(max_length=8,default="none")
  url     = models.URLField(null=True,blank=True)

  @models.permalink
  def get_absolute_url(self):
    return ('show_wcag20')     

  class Meta:
        ordering = ['num']
        verbose_name="WCAG 2.0 Principle"
        verbose_name_plural="WCAG 2.0 Principles"
  
  def __str__(self):
      return 'Principle ' + str(self.num) + '. ' + self.title

  def save(self):
  
    self.number = str(self.num) + "."
      
    super(Principle, self).save() # Call the "real" save() method. 

  def number(self):
    return "%s."%(self.num)

  def guidelines_set(self):
    return self.guidelines.all()


from django.db import models
from django.contrib.auth.models import User
import re

## WCAG Guideline

class Guideline(models.Model):
  id      = models.AutoField(primary_key=True)
  
  principle = models.ForeignKey(Principle,related_name='guidelines')
  title     = models.CharField(max_length=200)
  num       = models.IntegerField()
  number    = models.CharField(max_length=8,default="none")
  url       = models.URLField(null=True,blank=True)
  slug      = models.SlugField(max_length=32)

  class Meta:
        ordering = ['principle__num', 'num']
        verbose_name="WCAG 2.0 Guideline"
        verbose_name_plural="WCAG 2.0 Guidelines"
  
  def __str__(self):
      return str(self.principle.num) + '.' + str(self.num) + ' ' + self.title

  def save(self):
  
    self.number = str(self.principle.num) + "." + str(self.num)
      
    super(Guideline, self).save() # Call the "real" save() method. 
     
  def requirements_set(self):
    return self.requirements.all()

  def get_rule_count(self):

    count = 0  

    for sc in self.success_criteria.all():
      for r in sc.rules.all():
        count += 1

    return count  

  def get_rules(self):

    rules = []

    for sc in self.success_criteria.all():
      for r in sc.rules.all():
        rules.append(r)

    return rules  


## WCAG Success Crieterion
WCAG20_LEVEL = (
    ('1', 'Level A'),
    ('2', 'Level AA'),
    ('3', 'Level AAA'),
)

## WCAG Success Crieterion
WCAG20_LEVEL_HTML_CODE = (
    ('1', '<abbr title="WCAG 2.0 Level A">A</abbr>'),
    ('2', '<abbr title="WCAG 2.0 Level AA">AA</abbr>'),
    ('3', '<abbr title="WCAG 2.0 Level AAA">AAA</abbr>'),
)

class SuccessCriterion(models.Model):
  id             = models.AutoField(primary_key=True)

  guideline      = models.ForeignKey(Guideline,related_name='success_criteria')
  title          = models.TextField()
  level          = models.CharField(max_length=2,choices=WCAG20_LEVEL)  
  num            = models.IntegerField()
  number         = models.CharField(max_length=8,default="none")
  url            = models.URLField(null=True,blank=True)
  url_meet       = models.URLField(null=True,blank=True)
  url_understand = models.URLField(null=True,blank=True)
  slug           = models.SlugField(max_length=32)

  class Meta:
        ordering = ['guideline__principle__num', 'guideline__num', 'num']
        verbose_name="WCAG 2.0 Success Criterion"
        verbose_name_plural="WCAG 2.0 Success Criteria"
  
  def __str__(self):
      return str(self.guideline.principle.num) + '.' + str(self.guideline.num) + '.' + str(self.num) + ' ' + self.title 


  def save(self):
  
    self.number = str(self.guideline.principle.num) + "." + str(self.guideline.num) + "." + str(self.num)
      
    super(SuccessCriterion, self).save() # Call the "real" save() method.  
         
  def get_rules(self):

    rules = []
    
    for r in self.rules.all():
      rules.append(r)

    return rules

  def get_related_rules(self):

    rules = []
    
    for r in self.related_rules.all():
      rules.append(r)

    return rules
    
  def show_level(self):
      for shortp, longp in WCAG20_LEVEL:
          if shortp == self.level:
              return longp

  def show_level_html(self):
      for shortp, longp in WCAG20_LEVEL_HTML_CODE:
          if shortp == self.level:
              return longp

  def show_number_html(self):
    return '<a href="' + self.url + '" target="_wcag20" title="' + self.title + '">' + self.number + '</a>'
              
  def show_success_criterion_html(self):
    html = '<a href="' + self.url + '" target="_wcag20">'
    html += str(self.guideline.principle.num) + '.' + str(self.guideline.num) + '.' + str(self.num) + ' ' + self.title
    html += '</a>'
    return html

             
             
  @staticmethod
  def get_by_wcag_number(num):
    parts = num.split('.')
    return SuccessCriterion.objects.get(num=parts[2],guideline__num=parts[1],guideline__principle__num=parts[0])

