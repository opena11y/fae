# reports/urls.py
from django.conf.urls import url
from .views import Profile

urlpatterns = [
    url(r'^profile/$', Profile.as_view(), name='account_profile'),
]