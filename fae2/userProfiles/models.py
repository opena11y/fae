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
from websiteResultGroups.models import WebsiteReportGroup
from reports.models             import WebsiteReport
from stats.models               import StatsUser
import markdown

import datetime

class UserProfile(models.Model):

    user          = models.OneToOneField(User, related_name="profile")

    account_type     = models.ForeignKey(AccountType, related_name="user_profiles")
    account_expires  = models.DateTimeField(null=True, blank=True)

    org           = models.CharField(max_length=128, blank=True)
    dept          = models.CharField(max_length=128, blank=True)
    email_announcements = models.BooleanField(default=True)

    timezone = TimeZoneField(default='America/Chicago')
    
    def __unicode__(self):
        return self.user.username  

    def get_active_reports(self):

        user_reports = WebsiteReport.objects.filter(user=self.user).filter(status='C')
        reports = user_reports[0:self.account_type.max_archive]
        old_reports  = user_reports[self.account_type.max_archive:]

        return [reports, old_reports] 
    
# creates new UserProfile when new user registers 
def user_registered_callback(sender, user, request, **kwargs):

    profile = UserProfile(user = user)
    profile.account_type = AccountType.objects.get(type_id=1)
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