# userProfile/urls.py
from django.conf.urls import url

from .views import UpdateUserProfile

urlpatterns = [
    url(r'^$', UpdateUserProfile.as_view(), name='user_profile'),
]

