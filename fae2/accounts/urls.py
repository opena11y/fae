# reports/urls.py
from django.conf.urls import url
from .views import UpdateUserProfileView
from .views import StatusView


urlpatterns = [
    url(r'^profile/$', UpdateUserProfileView.as_view(), name='user_profile'),
    url(r'^status/$',  StatusView.as_view(),            name='fae_status'),
]


