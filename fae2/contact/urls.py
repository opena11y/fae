# abouts/urls.py
from django.conf.urls import url
from .views import ContactFormView
from .views import ContactsView

urlpatterns = [ 
    url(r'^$', ContactFormView.as_view(),        name='contact_form'),
    url(r'^complete/$', ContactsView.as_view(),  name='contacts'),
]
