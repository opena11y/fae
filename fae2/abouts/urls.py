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

File: abouts/tests.py

Author: Jon Gunderson

"""


# abouts/urls.py
from __future__ import absolute_import
from django.conf.urls import url
from .views import ConceptsTerms
from .views import Disclaimer
from .views import Overview
from .views import Privacy
from .views import ReportIssues
from .views import Sharing
from .views import Versions

urlpatterns = [ 
    url(r'^$',            Overview.as_view(),       name='overview'),
    url(r'^concepts/$',   ConceptsTerms.as_view(),  name='concepts_terms'),
    url(r'^disclaimer/$', Disclaimer.as_view(),     name='disclaimer'),
    url(r'^issues/$',     ReportIssues.as_view(),   name='report_issues'),
    url(r'^privacy/$',    Privacy.as_view(),        name='privacy'),
    url(r'^sharing/$',    Sharing.as_view(),        name='sharing'),
    url(r'^versions/$',   Versions.as_view(),       name='versions'),
]
