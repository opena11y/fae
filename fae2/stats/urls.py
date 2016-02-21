# stats/urls.py
from django.conf.urls import url

from .views import ShowUsageStatistics

urlpatterns = [
    url(r'^$', ShowUsageStatistics.as_view(), name='usage_statistics'),
]

