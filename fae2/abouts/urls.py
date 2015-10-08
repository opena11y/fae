# abouts/urls.py
from django.conf.urls import url
from .views import Overview

urlpatterns = [
    url(r'^$', Overview.as_view(), name='overview'),
]
