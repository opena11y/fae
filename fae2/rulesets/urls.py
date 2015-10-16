# abouts/urls.py
from django.conf.urls import url
from .views import RulesetsView
from .views import RulesetView

urlpatterns = [
    url(r'^$', RulesetsView.as_view(), name='rulesets'),
    url(r'^ruleset/(?P<slug>\w+)/$', RulesetView.as_view(), name='ruleset'),
]
