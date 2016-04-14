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

from __future__ import absolute_import
"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import include, url
from django.contrib import admin

from fae2.settings import SHIBBOLETH_ENABLED


from reports import views

from accounts.views import Logout
from accounts.views import Login
from accounts.views import ShibbolethLogout
from accounts.views import ShibbolethLogin
from accounts.views import ShibbolethDiscovery

urlpatterns = [
    url(r'^admin/',   include(admin.site.urls)),
    # fae2 specific 
    url(r'^',           include('reports.urls')),
    url(r'^abouts/',    include('abouts.urls')),
    url(r'^contact/',   include('contact.urls')),
    url(r'^accounts/',  include('accounts.urls')),
    url(r'^rulesets/',  include('rulesets.urls')),
    url(r'^usage/',     include('stats.urls')),
]

if SHIBBOLETH_ENABLED: 
  urlpatterns += [
     url(r'^login/$',           ShibbolethLogin.as_view(),     name='login'),
     url(r'^logout/$',          ShibbolethLogout.as_view(),    name='logout'),
     url(r'^shib-discovery/$',  ShibbolethDiscovery.as_view(), name='shib_discovery'),
  ]
else:
  urlpatterns += [
    url(r'^accounts/',     include('registration.backends.hmac.urls')),
    url(r'^registration/', include('django.contrib.auth.urls')),
    url(r'^logout/$',      Logout.as_view(), name='logout'),
  ]
