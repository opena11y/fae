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

file: populate/pop_accounts.py

Author: Jon Gunderson

"""


from __future__ import print_function
from __future__ import absolute_import
import sys
import os
import django
from django.core.exceptions import ObjectDoesNotExist

fp = os.path.realpath(__file__)
path, filename = os.path.split(fp)

fae2_path = path.split('/populate')[0]
sys.path.append(fae2_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fae2.settings')
from django.conf import settings

django.setup()


"""This file is for populating the database with markup information
I empty it. Run as a standalone script!"""

from django.core.exceptions import ObjectDoesNotExist
from accounts.models import AccountType

from django.contrib.auth.models import User


def create_acount_type(type_id, self, shib, host, sponsor, title, permanent, archive, depth, pages, default, adv, protected ):


  try:
    atype = AccountType.objects.get(type_id=type_id)
    print("  Updating Account Type: " + title)

    atype.type   = type_id
    atype.title  = title

    atype.self_registration = self
    atype.shibboleth        = shib
    atype.self_hosted       = host
    atype.sponsor           = sponsor

    atype.max_archive   = archive
    atype.max_permanent = permanent
    atype.max_depth     = depth
    atype.max_pages     = pages

    atype.default       = default

    atype.advanced      = adv
    atype.protected     = protected

  except ObjectDoesNotExist:
    print("  Creating Account Type: " + title )
    atype = AccountType(type_id=type_id, self_registration=self, shibboleth=shib, self_hosted=host, sponsor=sponsor, title=title, max_archive=archive, max_permanent=permanent, max_depth=depth, max_pages=pages, default=default, advanced=adv, protected=protected)

  atype.save()
  return atype

def set_account_type_description(type_id, desc):
  try:
    atype = AccountType.objects.get(type_id=type_id)
    print("  Updating Account Type Description: " + atype.title)

    atype.description       = desc
    atype.save()

  except ObjectDoesNotExist:
    print("  Account type not found: " + acc_type )

create_acount_type(0, False, False, False, False,  'Anonymous',         1,  1, 1,    1, False,  False, False)
create_acount_type(1, True, False, False, False,   'Free',               2,  5, 2,   10, True,   False, False)
create_acount_type(2, True, False, False, False,   'Standard I',         5, 10, 3,   25, False,  False, False)
create_acount_type(3, True, False, False, False,   'Standard II',       10, 20, 3,   50, False,  False, False)
create_acount_type(4, True, False, False, False,   'Advanced I',        10, 20, 4,  100, False,   True, False)
create_acount_type(5, True, False, False, False,   'Advanced II',       20, 40, 5,  200, False,   True, False)
create_acount_type(6, True, False, False, False,   'Advanced III',      40, 80, 6,  400, False,   True, False)

create_acount_type(16, False, True, False, False, 'Institutional I: Small Size Institutions',   20, 40, 4,  100, False,   False, False)
create_acount_type(17, False, True, False, False, 'Institutional I: Medium Size Institutions',  20, 40, 4,  100, False,   False, False)
create_acount_type(18, False, True, False, False, 'Institutional I: Large Size Institutions',        20, 40, 4,  100, False,   False, False)

create_acount_type(32, False, False, True, False, 'Self-Hosted',    20, 40, 5,  400, False,   True, False)

create_acount_type(64, False, False, False, True, 'Sponsor: Bronze',  40, 80, 5, 800, False, True, False)
create_acount_type(65, False, False, False, True, 'Sponsor: Sliver',  40, 80, 5, 800, False, True, False)
create_acount_type(66, False, False, False, True, 'Sponsor: Gold',    40, 80, 5, 800, False, True, False)

set_account_type_description(1, """Free version provides basic website evaluation for any user.  If you use FAE and/or AInspector Sidebar on a regular basis we ask that you help support the development and maintenance of the tools by purchasing a paid level subscriptions.""")

set_account_type_description(2, """The Standard I subscription is provides an inidividual, educational and/or other organization with more extensive website evaluation services including deeper spidering of pages in a website, higher maximum number of pages, more saved and permanent reports.""")

set_account_type_description(3, "")
  
set_account_type_description(16, """For educational institutions less than 5,000 students.""")
set_account_type_description(17, """For educational institutions of 5,000 students to 10,000 students.""")
set_account_type_description(18, """For educational institutions of over 10,000 students .""")