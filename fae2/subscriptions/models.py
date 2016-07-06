"""
Copyright 2014-2016 University of Illinois

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

file: subscriptions/models.py

Author: Jon Gunderson

"""

from __future__ import unicode_literals

from django.db         import models
from accounts.models   import AccountType

# Create your models here.

class Subscription(models.Model):
    id = models.AutoField(primary_key=True)

    subscription_id = models.IntegerField(default=0)

    description        = models.TextField(blank=True, default="")
    description_html   = models.TextField(blank=True, default="")

    account_type  = models.OneToOneField(AccountType, related_name="subscriptions")

    one_month     = models.IntegerField(default=0)
    three_month   = models.IntegerField(default=0)
    six_month     = models.IntegerField(default=0)
    twelve_month  = models.IntegerField(default=0)

    class Meta:
        verbose_name        = "Subscription"
        verbose_name_plural = "Subscriptions"
        ordering = ['account_type']
    
    def __str__(self):
        return 'Subscription: ' + self.account_type.title

    def save(self):
      
        if self.description:   
            self.description_html  = markdown.markdown(self.description)
      
        super(Subscription, self).save() # Call the "real" save() method.  
