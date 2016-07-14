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

File: accounts/urls.py

Author: Jon Gunderson

"""

# accounts/urls.py
from __future__ import absolute_import
from django.conf.urls import url

from .views import UpdateUserProfileView
from .views import UpdateAccountTypeView

from .views import DonateView
from .views import DonateSuccessView
from .views import DonateFailView

from .views import StatusView
from .views import UserInformationView
from .views import AllUserInformationView


urlpatterns = [
    url(r'^$',         UpdateUserProfileView.as_view(),   name='user_profile'),
    url(r'^update/$',  UpdateAccountTypeView.as_view(),   name='update_account_type'),

    url(r'^donate/$',          DonateView.as_view(),        name='donate'),
    url(r'^donate/success/$',  DonateSuccessView.as_view(), name='donate_success'),
    url(r'^donate/fail/$',     DonateFailView.as_view(),    name='donate_fail'),

    url(r'^status/$',         StatusView.as_view(),              name='fae_status'),
    url(r'^all-user-info/$',  AllUserInformationView.as_view(),  name='all_user_information'),
    url(r'^user-info/(?P<user_id>[\d-]+)/$',  UserInformationView.as_view(),   name='user_information'),
]


