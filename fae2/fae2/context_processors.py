from django.contrib.sites.models import Site
from userProfiles.models import UserProfile

from fae2.settings import ANONYMOUS
from fae2.settings import SELF_REGISTRATION
from fae2.settings import SHIBBOLETH


def site(request):
    return {
        'site': Site.objects.get_current()
    }

def anonymous(request):
	return {
		'anonymous': ANONYMOUS
	}

def self_registration(request):
	return {
		'self_registration': SELF_REGISTRATION
	}

def shibboleth(request):
	return {
		'shibboleth': SHIBBOLETH
	}

