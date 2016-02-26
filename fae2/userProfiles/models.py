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
"""

from django.db import models
from django.contrib.auth.models import User
from registration.signals import user_registered
from timezone_field import TimeZoneField
from websiteResultGroups.models import WebsiteReportGroup

## User Profile
# The built-in Django User relation:

#class User(models.Model):
#   username      = models.CharField(max_length=30, unique=True)
#   first_name    = models.CharField(max_length=30, blank=True)
#   last_name     = models.CharField(max_length=30, blank=True)
#   email         = models.EmailField(blank=True)
#   password      = models.CharField(max_length=128)
#   is_staff      = models.BooleanField(default=False)
#   is_active     = models.BooleanField(default=True)
#   is_superuser  = models.BooleanField(default=False)
#   last_login    = models.DateTimeField()
#   date_joined   = models.DateTimeField()

# Custom classes for FAE


ACCT_TYPE_CHOICES = (
  (1, 'Standard'),
  (2, 'Level 2'),
  (3, 'Level 3'),
  (4, 'Level 4'),
  (5, 'Maximum'),
)


class UserProfile(models.Model):

    user          = models.OneToOneField(User, related_name="profile")
    acct_type     = models.IntegerField(choices=ACCT_TYPE_CHOICES, default=1)
    org           = models.CharField(max_length=128, blank=True)
    dept          = models.CharField(max_length=128, blank=True)
    email_announcements = models.BooleanField(default=True)

    max_archive = models.IntegerField(default=5)
    max_saved   = models.IntegerField(default=10)

    timezone = TimeZoneField(default='America/Chicago')
    
    multiple_urls_enabled           = models.BooleanField(default=False)
    website_authorization_enabled   = models.BooleanField(default=False)
    advanced_enabled                = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.username  


    def get_account_type(self):
      for shortp, longp in ACCT_TYPE_CHOICES:
          if shortp == self.acct_type:
              return longp
    
    
# creates new UserProfile when new user registers 
def user_registered_callback(sender, user, request, **kwargs):

    profile = UserProfile(user = user)
    profile.acct_type = 1
    profile.org = ''
    profile.save()
    profile.add_website_report_group()
   
    # Update first and last name for user
    user.first_name = request.POST['first_name'] 
    user.last_name = request.POST['last_name']
    user.save()
 
user_registered.connect(user_registered_callback)  