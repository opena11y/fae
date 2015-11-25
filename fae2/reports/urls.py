# reports/urls.py
from django.conf.urls import url
from .views import RunReportView
from .views import RunAnonymousReportView
from .views import ProcessingReportView
from .views import ArchivedReportView
from .views import ManageReportView
from .views import ReportView

urlpatterns = [
    url(r'^$',                       RunReportView.as_view(),          name='run_report'),
    url(r'^anonymous/$',             RunAnonymousReportView.as_view(), name='run_anonymous_report'),
    url(r'^processing/$',            ProcessingReportView.as_view(),   name='processing_report'),
    url(r'^archived/$',              ArchivedReportView.as_view(),     name='archived_report'),
    url(r'^manage/$',                ManageReportView.as_view(),       name='manage_report'),
    url(r'^report/(?P<slug>\w+)/$',  ReportView.as_view(),             name='show_report'),
]