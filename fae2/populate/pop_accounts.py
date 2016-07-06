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


def create_acount_type(type_id, title, archive, permanent, depth, pages, default, adv, protected ):


  try:
    atype = AccountType.objects.get(type_id=type_id)
    print("  Updating Account Type: " + title)

    atype.type   = type_id
    atype.title  = title

    atype.max_archive   = archive
    atype.max_permanent = permanent
    atype.max_depth     = depth
    atype.max_pages     = pages

    atype.default       = default

    atype.advanced      = adv
    atype.protected     = protected

  except ObjectDoesNotExist:
    print("  Creating Account Type: " + title )
    atype = AccountType(type_id=type_id, title=title, max_archive=archive, max_permanent=permanent, max_depth=depth, max_pages=pages, default=default, advanced=adv, protected=protected)

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


create_acount_type(0, 'Anonymous',       1,  1, 1,    1, False,  False, False )
create_acount_type(1, 'Trial',           2,  5, 2,   25, True,   False, False )
create_acount_type(2, 'Non-Commercial',  5, 10, 3,   50, False,  False, False )
create_acount_type(3, 'Commercial',      5, 10, 3,  100, False,  False, False )
create_acount_type(4, 'Advanced',       10, 20, 4,  200, False,   True, False )
create_acount_type(5, 'Sustainer',      20, 40, 5,  400, False,   True, False )
create_acount_type(6, 'Founder',        40, 80, 6,  800, False,   True, False )
create_acount_type(7, 'Special I',      40, 80, 6, 1600, False,   True, False )
create_acount_type(16, 'Shibboleth',    20, 40, 5,  400, False,   True, False )

set_account_type_description(1, """
* No cost trial version for determining if FAE is useful to you for understanding the accessibility of your online resources.  
* If you use FAE and/or AInspector Sidebar on a regular we ask that you help support the development and maintenance of the tools by purchasing on of the paid level subscriptions.""")
  
