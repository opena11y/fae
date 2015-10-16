import sys,os
import django
from django.core.exceptions import ObjectDoesNotExist

sys.path.append(os.path.abspath('..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fae2.settings')
from django.conf import settings

django.setup()

"""This file is for populating the database with markup information
I empty it. Run as a standalone script!"""

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.models import Site
from django.contrib.auth.models import User

users = (
('jongund', 'abc', 'jongund@illinois.edu', 'Jon', 'Gunderson', True, True, True), 
('anonymous', 'GhE6*2@Vd', '', 'Anonymous', 'Anonymous', True, False, False), 
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

        
def set_site(name, url):
    site = Site.objects.get_current()
    site.domain = url
    site.name = name
    site.save()

create_users(users)
set_site('FAE 2.0 (Jon Development Prototype)', 'http://localhost:8000')


