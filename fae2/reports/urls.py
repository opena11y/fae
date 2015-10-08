# reports/urls.py
from django.conf.urls import url
from .views import RunReport

urlpatterns = [
    url(r'^$', RunReport.as_view(), name='run_report'),
]