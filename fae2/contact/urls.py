# abouts/urls.py
from django.conf.urls import url
from .views import ContactFormView
from .views import ResponseFormView
from .views import ResponsesView

urlpatterns = [ 
    url(r'^$', ContactFormView.as_view(),                      name='contact_form'),
    url(r'^respond/all/$',         ResponsesView.as_view(),    name='responses'),
    url(r'^respond/(?P<pk>\d+)/$', ResponseFormView.as_view(), name='response_form'),
]
