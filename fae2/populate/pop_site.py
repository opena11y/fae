import sys,os
import django
import json
from os.path import join, abspath, dirname

from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ImproperlyConfigured

sys.path.append(os.path.abspath('..'))
# print('\nSystem Paths\n' + str(sys.path) + '\n')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fae2.settings')
from django.conf import settings
django.setup()

"""This file is for populating the database with markup information
I empty it. Run as a standalone script!"""

from django.core.exceptions      import ObjectDoesNotExist
from django.contrib.sites.models import Site
from django.contrib.auth.models  import User
from userProfiles.models         import UserProfile
from websiteResultGroups.models  import WebsiteReportGroup
from stats.models                import StatsUser

# JSON-based secrets module
with open(join(settings.BASE_DIR,"secrets.json")) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    """(Get the secret variable or return explicit exception.)"""
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} enviroment variable".format(setting)
        raise ImproperlyConfigured


users = (
(get_secret('ADMIN_USER_NAME'), get_secret('ADMIN_PASSWORD'), get_secret('ADMIN_EMAIL'), get_secret('ADMIN_FIRST_NAME'), get_secret('ADMIN_LAST_NAME'), True, True, True), 
('anonymous', get_secret('ANONYMOUS_PASSWORD'), '', 'Anonymous', 'Anonymous', True, False, False), 
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
set_site(get_secret('SITE_NAME'), get_secret('SITE_URL'))


