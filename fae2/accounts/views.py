from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth import logout 

class Logout(TemplateView):
    template_name = 'registration/logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(Logout, self).get(request, *args, **kwargs)


class Profile(TemplateView):
    template_name = 'accounts/profile.html'    