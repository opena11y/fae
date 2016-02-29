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

import sys
import os
import django
from django.core.exceptions import ObjectDoesNotExist
import json

fp = os.path.realpath(__file__)
path, filename = os.path.split(fp)

fae2_path = path.split('/populate')[0]
sys.path.append(fae2_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fae2.settings')
from django.conf import settings

django.setup()

"""This file is for populating the database with markup information
I empty it. Run as a standalone script!"""

from django.core.exceptions      import ObjectDoesNotExist
from django.core.exceptions      import ImproperlyConfigured
from django.contrib.sites.models import Site
from django.contrib.auth.models  import User
from userProfiles.models         import UserProfile
from websiteResultGroups.models  import WebsiteReportGroup
from stats.models                import StatsUser



users = (
(settings.ADMIN_USER_NAME, settings.ADMIN_PASSWORD, settings.ADMIN_EMAIL, settings.ADMIN_FIRST_NAME, settings.ADMIN_LAST_NAME, True, True, True), 
('anonymous', settings.ANONYMOUS_PASSWORD, '', 'Anonymous', 'Anonymous', True, False, False), 
)


def create_users(users):
    
    for person in users:
        try:
          print("Update User: " + person[0])
          user = User.objects.get(username=person[0])
          user.email        = person[2]
          user.first_name   = person[3]
          user.last_name    = person[4]
          user.is_active    = person[5]
          user.is_superuser = person[6]
          user.is_staff     = person[7]
        except ObjectDoesNotExist:
          print("Create User: " + person[0])
          user = User(username=person[0], email=person[2], first_name=person[3], last_name=person[4], is_active=person[5], is_superuser=person[6], is_staff=person[7])
          user.set_password(person[1])
        user.save()

        try:
          profile = UserProfile.objects.get(user=user)
        except:
          profile = UserProfile(user=user)
        profile.save()   

        try:
          stats = StatsUser.objects.get(user=user)
        except:
          wsrg =  WebsiteReportGroup(title="Summary of results for " + str(user))
          wsrg.save()
          stats = StatsUser(user=user, ws_report_group=wsrg)  
        stats.save()   

        
def set_site(name, url):
    site = Site.objects.get_current()
    site.domain = url
    site.name = name
    site.save()

create_users(users)
set_site(settings.SITE_NAME, settings.SITE_URL)


