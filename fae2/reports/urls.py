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

file: reports/urls.py

Author: Jon Gunderson

"""

# reports/urls.py
from __future__ import absolute_import
from django.conf.urls import url

from .views import RunReportView
from .views import RunAnonymousReportView
from .views import RunRefererReportView

from .views import ProcessingAnonymousReportView
from .views import ProcessingReportView

from .views import ArchivedReportView
from .views import ManageReportView

from .views import ProcessingStatusJSON
from .views import ProcessingStatusAllJSON

from .views import SetReportPermanentView
from .views import DeleteReportView
from .views import RestoreReportView

from .views import URLInformationView

from .views import ReportJSON
from .views import ReportNotFoundView

from .views import ReportRulesView
from .views import ReportRulesGroupView
from .views import ReportRulesGroupRuleView
from .views import ReportRulesGroupRulePageView

from .views_csv import ReportRulesViewCSV
from .views_csv import ReportRulesGroupViewCSV
from .views_csv import ReportRulesGroupRuleViewCSV
from .views_csv import ReportRulesGroupRulePageViewCSV

from .views import ReportPagesView
from .views import ReportPagesGroupView

from .views import ReportPageView
from .views import ReportPageGroupView
from .views import ReportPageGroupRuleView

from .views_csv import ReportPagesViewCSV
from .views_csv import ReportPagesGroupViewCSV

from .views_csv import ReportPageViewCSV
from .views_csv import ReportPageGroupViewCSV
from .views_csv import ReportPageGroupRuleViewCSV

from fae2.settings import ANONYMOUS_ENABLED
from fae2.settings import SELF_REGISTRATION_ENABLED
from fae2.settings import PAID_SUBSCRIPTION_ENABLED
from fae2.settings import SHIBBOLETH_ENABLED

urlpatterns = [
    url(r'^$',                RunReportView.as_view(),         name='run_report'),
    url(r'^processing/$',     ProcessingReportView.as_view(),  name='processing_reports'),
    url(r'^evaluate/link/$',  RunRefererReportView.as_view(),  name='run_referer_report'),

    url(r'^processing/status/all/$',              ProcessingStatusAllJSON.as_view(), name='processing_status_all'),
    url(r'^processing/status/(?P<report>\w+)/$',  ProcessingStatusJSON.as_view(),    name='processing_status'),


    url(r'^archived/$',              ArchivedReportView.as_view(),     name='archived_reports'),
    url(r'^manage/$',                ManageReportView.as_view(),       name='manage_reports'),


    url(r'^report/(?P<report>\w+)/permanent/(?P<value>\w+)/$',   SetReportPermanentView.as_view(),  name='report_permanent'),
    url(r'^report/(?P<report>\w+)/delete/$',    DeleteReportView.as_view(),        name='report_delete'),
    url(r'^report/(?P<report>\w+)/restore/$',   RestoreReportView.as_view(),      name='report_restore'),

    url(r'^summary/(?P<report>\w+)/error/$',   ReportNotFoundView.as_view(),  name='report_not_found'),

    url(r'^summary/(?P<report>\w+)/(?P<view>\w+)/urls/$',                                                    URLInformationView.as_view(),  name='report_url_information'),

    url(r'^summary/(?P<report>\w+)/json/$', ReportJSON.as_view(),  name='report_json'),

    url(r'^summary/(?P<report>\w+)/(?P<view>\w+)/$',                                                             ReportRulesView.as_view(),               name='report_rules'),
    url(r'^summary/(?P<report>\w+)/(?P<view>\w+)/csv/$',                                                         ReportRulesViewCSV,                      name='report_rules_csv'),
    url(r'^summary/(?P<report>\w+)/(?P<view>\w+)/(?P<group>\w+)/$',                                              ReportRulesGroupView.as_view(),          name='report_rules_group'),
    url(r'^summary/(?P<report>\w+)/(?P<view>\w+)/(?P<group>\w+)/csv/$',                                          ReportRulesGroupViewCSV,                 name='report_rules_group_csv'),
    url(r'^summary/(?P<report>\w+)/(?P<view>\w+)/(?P<group>\w+)/rule/(?P<rule>\w+)/$',                           ReportRulesGroupRuleView.as_view(),      name='report_rules_group_rule'),
    url(r'^summary/(?P<report>\w+)/(?P<view>\w+)/(?P<group>\w+)/rule/(?P<rule>\w+)/csv/$',                       ReportRulesGroupRuleViewCSV,             name='report_rules_group_rule_csv'),
    url(r'^summary/(?P<report>\w+)/(?P<view>\w+)/(?P<group>\w+)/rule/(?P<rule>\w+)/page/(?P<page>[\d-]+)/$',     ReportRulesGroupRulePageView.as_view(),  name='report_rules_group_rule_page'),
    url(r'^summary/(?P<report>\w+)/(?P<view>\w+)/(?P<group>\w+)/rule/(?P<rule>\w+)/page/(?P<page>[\d-]+)/csv/$', ReportRulesGroupRulePageViewCSV,         name='report_rules_group_rule_page_csv'),

    url(r'^pages/(?P<report>\w+)/(?P<view>\w+)/all/$',                                                     ReportPagesView.as_view(),          name='report_pages'),
    url(r'^pages/(?P<report>\w+)/(?P<view>\w+)/all/csv/$',                                                 ReportPagesViewCSV,                 name='report_pages_csv'),
    url(r'^pages/(?P<report>\w+)/(?P<view>\w+)/(?P<group>\w+)/$',                                          ReportPagesGroupView.as_view(),     name='report_pages_group'),
    url(r'^pages/(?P<report>\w+)/(?P<view>\w+)/(?P<group>\w+)/csv/$',                                      ReportPagesGroupViewCSV,            name='report_pages_group_csv'),
    url(r'^pages/(?P<report>\w+)/(?P<view>\w+)/all/page/(?P<page>[\d-]+)/$',                               ReportPageView.as_view(),           name='report_page'),
    url(r'^pages/(?P<report>\w+)/(?P<view>\w+)/all/page/(?P<page>[\d-]+)/csv/$',                           ReportPageViewCSV,                  name='report_page_csv'),
    url(r'^pages/(?P<report>\w+)/(?P<view>\w+)/(?P<group>\w+)/page/(?P<page>[\d-]+)/$',                    ReportPageGroupView.as_view(),      name='report_page_group'),
    url(r'^pages/(?P<report>\w+)/(?P<view>\w+)/(?P<group>\w+)/page/(?P<page>[\d-]+)/csv/$',                ReportPageGroupViewCSV,             name='report_page_group_csv'),
    url(r'^pages/(?P<report>\w+)/(?P<view>\w+)/(?P<group>\w+)/page/(?P<page>[\d-]+)/(?P<rule>\w+)/$',      ReportPageGroupRuleView.as_view(),  name='report_page_group_rule'),
    url(r'^pages/(?P<report>\w+)/(?P<view>\w+)/(?P<group>\w+)/page/(?P<page>[\d-]+)/(?P<rule>\w+)/csv/$',  ReportPageGroupRuleViewCSV,         name='report_page_group_rule_csv'),
]

if ANONYMOUS_ENABLED:
  urlpatterns += [
    url(r'^anonymous/$',             RunAnonymousReportView.as_view(),        name='run_anonymous_report'),
    url(r'^anonymous/processing/$',  ProcessingAnonymousReportView.as_view(), name='processing_anonymous_reports'),
  ]
