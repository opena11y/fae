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

file: populate/pop_subscriptions.py

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

from accounts.models      import AccountType
from subscriptions.models import Subscription

from django.contrib.auth.models import User


def create_subscription(sub_id, one, three, six, twelve):

  try:
    atype = AccountType.objects.get(type_id=sub_id)
  except ObjectDoesNotExist:
    print("Account Type not found for: " + str(sub_id))
    return


  try:
    sub = Subscription.objects.get(subscription_id=sub_id)
    print("  Updating Subscription: " + str(sub_id))

    sub.account_type  = atype

    sub.one_month     = one
    sub.three_month   = three
    sub.six_month     = six
    sub.twelve_month  = twelve

  except ObjectDoesNotExist:
    print("  Creating Subscription: " + str(sub_id) )
    sub = Subscription(subscription_id=sub_id, account_type=atype, one_month=one, three_month=three, six_month=six, twelve_month=twelve)

  sub.save()
  return sub

def set_subscription_description(sub_id, desc):
  try:
    sub = Subscription.objects.get(subscription_id=sub_id)
    print("  Updating Subscription Description: " + sub.account_type.title)

    sub.description       = desc
    sub.save()

  except ObjectDoesNotExist:
    print("  Subscription not found: " + str(sub_id) )


create_subscription( 0,    0,    0,    0,    0)
create_subscription( 1,   30,   80,  140,  240)
create_subscription( 2,   60,  160,  280,  480)
create_subscription( 3,   90,  240,  420,  720)
create_subscription( 4,  120,  320,  560,  960)
create_subscription( 5,  150,  400,  700, 1200)
create_subscription( 6,  240,  640, 1200, 1920)
create_subscription( 7,  480, 1280, 2400, 3840)
create_subscription(16,   20,   40,    5,  400)

    