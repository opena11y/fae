# reports/urls.py
from django.conf.urls import url
from .views import RunReportView
from .views import RunAnonymousReportView
from .views import ProcessingReportView
from .views import ProcessingStatusView
from .views import ArchivedReportView
from .views import ManageReportView
from .views import URLSummaryView

from .views import ReportView
from .views import ReportGroupView
from .views import ReportGroupRuleView
from .views import ReportGroupRulePageView

from .views import ReportPageView
from .views import ReportPageGroupView
from .views import ReportPageGroupRuleView

urlpatterns = [
    url(r'^$',                       RunReportView.as_view(),          name='run_report'),
    url(r'^anonymous/$',             RunAnonymousReportView.as_view(), name='run_anonymous_report'),
    url(r'^processing/$',            ProcessingReportView.as_view(),   name='processing_reports'),
    url(r'^status/json/$',           ProcessingStatusView.as_view(),   name='processing_status_json'),    
    url(r'^archived/$',              ArchivedReportView.as_view(),     name='archived_reports'),
    url(r'^manage/$',                ManageReportView.as_view(),       name='manage_reports'),

    url(r'^report/(?P<slug>\w+)/urls/$',  URLSummaryView.as_view(),    name='show_url_summary'),

    url(r'^report/(?P<report>\w+)/(?P<view>\w+)/$',                                                         ReportView.as_view(),              name='show_report'),
    url(r'^report/(?P<report>\w+)/(?P<view>\w+)/(?P<group>\w+)/$',                                          ReportGroupView.as_view(),         name='show_report_group'),
    url(r'^report/(?P<report>\w+)/(?P<view>\w+)/(?P<group>\w+)/rule/(?P<rule>\w+)/$',                       ReportGroupRuleView.as_view(),     name='show_report_group_rule'),
    url(r'^report/(?P<report>\w+)/(?P<view>\w+)/(?P<group>\w+)/rule/(?P<rule>\w+)/page/(?P<page>[\d-]+)/$', ReportGroupRulePageView.as_view(), name='show_report_group_rule_page'),

    url(r'^report/(?P<report>\w+)/(?P<view>\w+)/page/(?P<page>[\d-]+)/$',                               ReportPageView.as_view(),           name='show_report_page'),
    url(r'^report/(?P<report>\w+)/(?P<view>\w+)/page/(?P<page>[\d-]+)/(?P<group>\w+)/$',                ReportPageGroupView.as_view(),      name='show_report_page_group'),
    url(r'^report/(?P<report>\w+)/(?P<view>\w+)/page/(?P<page>[\d-]+)/(?P<group>\w+)/(?P<rule>\w+)/$',  ReportPageGroupRuleView.as_view(),  name='show_report_page_group_rule'),

]