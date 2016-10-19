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

file: userProfiles/models.py

Author: Jon Gunderson

"""

from __future__                 import absolute_import
from django.db                  import models
from django.contrib.auth.models import User
from registration.signals       import user_registered
from timezone_field             import TimeZoneField


from accounts.models            import AccountType
from subscriptions.models       import Payment
from websiteResultGroups.models import WebsiteReportGroup
from reports.models             import WebsiteReport
from stats.models               import StatsUser
from django.contrib.sites.models import Site

from contact.models              import Announcement


from django.core.urlresolvers import reverse
from django.template.loader   import render_to_string

from django.db.models import Q

from django.contrib import messages

import markdown

from fae2.settings import DEFAULT_ACCOUNT_TYPE

from django.core.mail import send_mail
from fae2.settings import EMAIL_HOST_USER
from fae2.settings import ADMIN_EMAIL


from datetime import datetime 

from datetime import date

SUBSCRIPTION_STATUS_CHOICES = (
    ('FREE',    'Free'),
    ('CURRENT',  'Current'),
    ('EXPIRED',  'Expired')
)

class UserProfile(models.Model):

    user          = models.OneToOneField(User, related_name="profile")

    account_type             = models.ForeignKey(AccountType, related_name="user_profiles")
    enable_any_account_types = models.BooleanField(default=False)
    
    subscription_start      = models.DateField(null=True, blank=True)
    subscription_end        = models.DateField(null=True, blank=True)
    subscription_payments   = models.IntegerField(default=0) # in dollars
    subscription_daily_rate = models.IntegerField(default=0) # in cents
    subscription_status     = models.CharField(max_length=8, choices=SUBSCRIPTION_STATUS_CHOICES, default="FREE")
    subscription_days       = models.IntegerField(default=0)

    top_level_domain = models.CharField(max_length=8, null=True, blank=True)
    domain           = models.CharField(max_length=64, null=True, blank=True)

    org                 = models.CharField(max_length=128, blank=True)
    dept                = models.CharField(max_length=128, blank=True)
    email_announcements = models.BooleanField(default=True)

    timezone = TimeZoneField(default='America/Chicago')
    
    def __unicode__(self):
        return self.user.username  

    def save(self):
      
        if self.user.email and not self.domain:
            self.set_domain_info()
      
        super(UserProfile, self).save() # Call the "real" save() method.  

    def set_domain_info(self):
        email = self.user.email

        if email:
            email = email.strip()
            parts = email.split('.')
            l = len(parts)
            if l > 1:
                self.top_level_domain = parts[l-1] 
                parts = parts[l-2].split('@')
                self.domain = parts[len(parts)-1]
                self.save()

    def set_payments(self, amount):
        self.subscription_payments = amount
        self.update_daily_rate()
    
    def add_payment(self, amount):
        self.subscription_payments += amount
        self.update_daily_rate()

    def subtract_payment(self, amount):
        self.subscription_payments -= amount

        if self.subscription_payments < 0:
            self.subscription_payments = 0 

        self.update_daily_rate()

    def update_subscription_status(self):
        self.enable_any_account_types = True  

        if self.subscription_end:
            self.enable_any_account_types = False  

            date1 = date(self.subscription_end.year, self.subscription_end.month, self.subscription_end.day)
            date2 = date.today()
            delta = date1 - date2

            self.subscription_days = delta.days

            if self.subscription_days >= 0:
                self.subscription_status = 'CURRENT'            
            else:
                self.subscription_status     = 'EXPIRED'
                self.subscription_payments   = 0
                self.subscription_daily_rate = 0
                self.account_type            = AccountType.objects.get(type_id=1)     

            if self.subscription_days < 7:
                self.enable_any_account_types = True  

        self.save() 
        
        self.update_daily_rate()

        return self.subscription_status

    def get_last_subscription(self):
        try:
            payments = Payment.objects.filter(Q(status='PMT_APPROV') | Q(status='PMT_NOCOST'), user=self.user).latest('reference_time')
        except:
            payments = False

        if payments:
            return payments
            
        return payments


    def check_for_subscription_messages(self, request):

        subscription_url = reverse('update_subscription')

        self.update_subscription_status()

        if self.subscription_status == 'CURRENT' and self.subscription_days < 8:
            messages.warning(request, render_to_string('accounts/subscription_current.txt', {'url': subscription_url, 'days': self.subscription_days})) 
        elif self.subscription_status == 'EXPIRED' and self.subscription_days == -1:
            messages.warning(request, render_to_string('accounts/subscription_expired.txt', {'url': subscription_url, 'days': self.subscription_days})) 

    def check_for_email_subscription_notifications(self):

        topic = ""
        
        if self.subscription_status == 'CURRENT':
            if self.subscription_days == 7:
                topic = "FAE subscription expires in " + str(self.subscription_days) + "days"
            elif self.subscription_days == 1:
                topic = "FAE subscription expires in one day"
            elif self.subscription_days == 0:
                topic = "FAE subscription expires today"

        if self.subscription_status == 'EXPIRED' and self.subscription_days == -1:              
            topic = "FAE subscription expired yesterday"
              
        if topic:
            site = Site.objects.get_current()
            message = render_to_string('accounts/email_message.txt', {'user_profile': self, 'subscription_url': str(site) + reverse('update_subscription') })
            send_mail(topic, message, EMAIL_HOST_USER, [self.user.email], fail_silently=False)        

        return


    def update_daily_rate(self):
        self.subscription_daily_rate = 0;

        if self.subscription_payments > 0 and self.subscription_end and self.subscription_start:
            date1 = date(self.subscription_end.year, self.subscription_end.month, self.subscription_end.day)
            date2 = date(self.subscription_start.year, self.subscription_start.month, self.subscription_start.day)
            delta = date1 - date2

            if delta.days > 0:
              self.subscription_daily_rate = (100 * self.subscription_payments) / delta.days

        self.save()        


    def get_active_reports(self):

        user_reports = WebsiteReport.objects.filter(user=self.user).filter(status='C')
        reports = user_reports[0:self.account_type.max_archive]
        old_reports  = user_reports[self.account_type.max_archive:]

        return [reports, old_reports] 

 

    
# creates new UserProfile when new user registers 
def user_registered_callback(sender, user, request, **kwargs):

    profile = UserProfile(user = user)
    profile.account_type = AccountType.objects.get(type_id=DEFAULT_ACCOUNT_TYPE)
    profile.org = ''
    profile.save()
   
    # Update first and last name for user
    user.first_name = request.POST['first_name'] 
    user.last_name = request.POST['last_name']
    user.save()

    wsrg =  WebsiteReportGroup(title="Summary of results for " + str(user))
    wsrg.save()
    user_stats = StatsUser(user=user, ws_report_group=wsrg)  
    user_stats.save()   

 
user_registered.connect(user_registered_callback)  