from django.contrib.sites.models import Site
from userProfiles.models import UserProfile

from fae2.settings import ANONYMOUS_ENABLED
from fae2.settings import SELF_REGISTRATION_ENABLED
from fae2.settings import SHIBBOLETH_ENABLED


def site(request):
    return {
        'site': Site.objects.get_current()
    }

def anonymous(request):
	return {
		'anonymous_enabled': ANONYMOUS_ENABLED
	}

def self_registration(request):
	return {
		'self_registration_enabled': SELF_REGISTRATION_ENABLED
	}

def shibboleth(request):
	return {
		'shibboleth_enabled': SHIBBOLETH_ENABLED
	}

