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
from django.contrib.auth.models import User

import markdown
import datetime

import string
import random

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

from accounts.models   import AccountType

# Create your models here.

class SubscriptionRate(models.Model):
    id = models.AutoField(primary_key=True)

    subscription_id    = models.IntegerField(default=0)

    description        = models.TextField(blank=True, default="")
    description_html   = models.TextField(blank=True, default="")

    account_type  = models.OneToOneField(AccountType, related_name="subscription_rate")

    one_month     = models.IntegerField(default=0)
    three_month   = models.IntegerField(default=0)
    six_month     = models.IntegerField(default=0)
    twelve_month  = models.IntegerField(default=0)

    class Meta:
        verbose_name        = "Subscription Rate"
        verbose_name_plural = "Subscription Rates"
        ordering = ['account_type']
    
    def __str__(self):
        return 'Subscription Rate: ' + self.account_type.title

    def save(self):
      
        if self.description:   
            self.description_html  = markdown.markdown(self.description)
      
        super(SubscriptionRate, self).save() # Call the "real" save() method.  

PAYMENT_TYPE = (
    ('DON', 'Donation'),
    ('SUB', 'Subscription'),
)

PAYMENT_STATUS = (
    ('NEW',      'New un-initialized payment transaction'),
    ('INIT',     'Transaction is ready for payment'),
    ('SUBMIT',   'Transaction has been sent for approval'),
    ('APPROV',   'Payment approved'),
    ('DECLINED', 'Payment declined'),
)

class Payment(models.Model):
    id = models.AutoField(primary_key=True)

    payment_id       = models.IntegerField(default=0)    

    user             = models.ForeignKey(User, related_name="payments", on_delete=models.CASCADE)

    status           = models.CharField(max_length=8, choices=PAYMENT_STATUS, default='NEW')
    payement_type    = models.CharField(max_length=8, choices=PAYMENT_TYPE, default='DON')

    account_type     = models.ForeignKey(AccountType, related_name="payments", null=True, blank=True, on_delete=models.CASCADE)

    reference_id     = models.CharField(max_length=50, blank=True, unique=True)
    transaction_id   = models.CharField(max_length=13, default="")
    token            = models.CharField(max_length=48, default="")

    amount           = models.IntegerField(default=-1)
    reconciliation   = models.IntegerField(default=-1)

    name             = models.CharField(max_length=60, default="")
    email            = models.EmailField(default="")
    show_donation    = models.BooleanField(default=False)

    transaction_date         = models.DateTimeField(auto_now_add=True, editable=False)
    account_expiration_date  = models.DateField(null=True, blank=True)


    class Meta:
        verbose_name        = "Payment"
        verbose_name_plural = "Payments"
        ordering = ['transaction_date']
    
    def __str__(self):
        return 'Payment: ' + self.name + ' (' + str(self.transaction_date.month) + '/' + str(self.transaction_date.day) + '/' + str(self.transaction_date.year) + ')'

    def save(self):

        self.reference_id   =  id_generator(50)     
     
        super(Payment, self).save() # Call the "real" save() method.         
