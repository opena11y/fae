from django.contrib.sites.models import Site
from userProfiles.models import UserProfile

def site(request):
    return {
        'site': Site.objects.get_current()
    }
