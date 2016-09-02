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
from subscriptions.models import SubscriptionRate
from userProfiles.models  import UserProfile

from django.contrib.auth.models import User

from fae2.settings import DEFAULT_ACCOUNT_TYPE

def create_subscription_rate(sub_id, one, three, six, twelve):

  try:
    atype = AccountType.objects.get(type_id=sub_id)
  except ObjectDoesNotExist:
    print("Account Type not found for: " + str(sub_id))
    return


  try:
    sub = SubscriptionRate.objects.get(subscription_id=sub_id)
    print("  Updating Subscription: " + str(sub_id))

    sub.account_type  = atype

    sub.one_month     = one
    sub.three_month   = three
    sub.six_month     = six
    sub.twelve_month  = twelve

  except ObjectDoesNotExist:
    print("  Creating Subscription: " + str(sub_id) )
    sub = SubscriptionRate(subscription_id=sub_id, account_type=atype, one_month=one, three_month=three, six_month=six, twelve_month=twelve)

  sub.save()
  return sub

def set_subscription_description(sub_id, desc):
  try:
    sub = SubscriptionRate.objects.get(subscription_id=sub_id)
    print("  Updating Subscription Description: " + sub.account_type.title)

    sub.description       = desc
    sub.save()

  except ObjectDoesNotExist:
    print("  Subscription not found: " + str(sub_id) )

def update_user_profiles():
  for u in User.objects.all():
    try:
      p = userProfile.objects.get(user=u)
    except:
      print("  Creating UserProfile for: " + u.username)

      p = UserProfile(user=u)
      if u.username == 'anonymous':
        p.account_type = AccountType.objects.get(type_id=0)
      else:  
        p.account_type = AccountType.objects.get(type_id=DEFAULT_ACCOUNT_TYPE)
      p.save()

create_subscription_rate( 0,    0,    0,    0,     0)
create_subscription_rate( 1,    0,    0,    0,     0)
create_subscription_rate( 2,   40,  110,  205,   360)
create_subscription_rate( 3,   70,  190,  360,   630)
create_subscription_rate( 4,  120,  325,  610,  1080)
create_subscription_rate( 5,  200,  540, 1020,  1800)
create_subscription_rate( 6,  300,  810, 1530,  2700)

create_subscription_rate(16,    0, 1000, 1800, 3200)
create_subscription_rate(17,    0, 2000, 3600, 6400)
create_subscription_rate(18,    0, 3000, 5400, 9600)

create_subscription_rate(32,    0, 2000, 3600, 6400)

update_user_profiles()