# abouts/urls.py
from django.conf.urls import url
from .views import Disclaimer
from .views import Overview
from .views import Privacy
from .views import Versions

urlpatterns = [
    url(r'^$', Overview.as_view(),   name='overview'),
    url(r'^disclaimer/$', Disclaimer.as_view(), name='disclaimer'),
    url(r'^privacy/$',    Privacy.as_view(),    name='privacy'),
    url(r'^versions/$', Versions.as_view(),   name='versions'),
]
