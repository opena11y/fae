"""
Copyright 2014-2016 University of Illinois

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

# accounts/views.py
from __future__ import absolute_import
from django.http import HttpResponse
from django.contrib.auth import logout 
from django.contrib import messages

from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy, reverse

from django.db.models import Q

from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic          import TemplateView
from django.views.generic          import FormView 
from django.views.generic          import RedirectView 
from django.contrib.auth.mixins    import LoginRequiredMixin


from django.contrib.auth.models import User
from userProfiles.models        import UserProfile
from stats.models               import StatsUser
from websiteResultGroups.models  import WebsiteReportGroup


from django.forms.models import inlineformset_factory


from django import forms


from websiteResults.models import WebsiteReport

from timezone_field import TimeZoneFormField

from reports.views import FAENavigationMixin

from fae2.settings import SITE_URL
from fae2.settings import SHIBBOLETH_SUPERUSER

from userProfiles.models import UserProfile
from stats.models        import StatsUser


# Create your views here.

class ShibbolethLogout(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        self.url = SITE_URL + '/Shibboleth.sso/Logout'
        return super(ShibbolethLogout, self).get_redirect_url(*args, **kwargs)


class ShibbolethLogin(RedirectView):

    def get_redirect_url(self, *args, **kwargs):

        user = self.request.user

        if user.username == SHIBBOLETH_SUPERUSER:
            user.is_staff     = True
            user.is_superuser = True
            user.save()

        try: 
            profile = UserProfile.objects.get(user=user)
        except:    
            profile = UserProfile(user=user)
            profile.save()

        try: 
            stats = StatsUser.objects.get(user=user)
        except ObjectDoesNotExist:
            wsrg =  WebsiteReportGroup(title="Summary of results for " + str(user))
            wsrg.save()
            stats = StatsUser(user=user, ws_report_group=wsrg)  
            stats.save()

        self.url = SITE_URL

        return super(ShibbolethLogin, self).get_redirect_url(*args, **kwargs)

class ShibbolethDiscovery(TemplateView):
    template_name = 'registration/shib_discovery.html'



class Logout(FAENavigationMixin, TemplateView):
    template_name = 'registration/logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(Logout, self).get(request, *args, **kwargs)

class Login(FAENavigationMixin, TemplateView):
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        context = super(Login, self).get_context_data(**kwargs)

        try:
          context['user']     = self.request.user
        except:
          context['user']     = 'none'
          
        return context  

class UserProfileForm(forms.Form):
    first_name          = forms.CharField(max_length=30)
    last_name           = forms.CharField(max_length=30)
    email               = forms.EmailField()
    org                 = forms.CharField(label="Organization", max_length=127, required=False)
    dept                = forms.CharField(label="Department", max_length=127, required=False)
    email_announcements = forms.BooleanField(required=False)
    timezone            = TimeZoneFormField()

class UpdateUserProfileView(LoginRequiredMixin, FAENavigationMixin, SuccessMessageMixin, FormView):
    template_name = 'accounts/my_account.html'
    form_class    = UserProfileForm

    success_url = reverse_lazy('user_profile')
    success_message = "Updated %(first_name)s %(last_name)s Profile"

    login_url = reverse_lazy('run_anonymous_report')
    redirect_field_name = "Anonymous Report"

    updated = False
    errors  = False

    def form_valid(self, form):

        user = self.request.user
        user.first_name = form.cleaned_data['first_name']
        user.last_name  = form.cleaned_data['last_name']
        user.email      = form.cleaned_data['email']
        user.save()

        profile           = user.profile
        profile.org       = form.cleaned_data['org']
        profile.dept      = form.cleaned_data['dept']
        profile.timezone  = form.cleaned_data['timezone']
        profile.email_announcements  = form.cleaned_data['email_announcements']
        profile.save()

        return super(UpdateUserProfileView, self).form_valid(form)
  


    def get_initial(self):
        # Populate ticks in BooleanFields
        user = self.request.user
        initial = {}
        initial['first_name'] = user.first_name
        initial['last_name']  = user.last_name
        initial['email']      = user.email
        initial['org']        = user.profile.org
        initial['dept']       = user.profile.dept
        initial['timezone']   = user.profile.timezone
        initial['email_announcements']        = user.profile.email_announcements
        return initial

    def get_context_data(self, **kwargs):
        context = super(UpdateUserProfileView, self).get_context_data(**kwargs)

        context['user_stats'] = StatsUser.objects.get(user=self.request.user)
        context['user_profile'] = UserProfile.objects.get(user=self.request.user)
        
        return context  

# ==============================================================
#
# Administration Status View
#
# ==============================================================

class StatusView(LoginRequiredMixin, FAENavigationMixin, TemplateView):
    template_name = 'accounts/status.html'

    def get_context_data(self, **kwargs):
        context = super(StatusView, self).get_context_data(**kwargs)

        reports = WebsiteReport.objects.all()

        context['initialized'] = reports.filter(Q(status='-') | Q(status='I'))
        context['processing']  = reports.filter(Q(status='A') | Q(status='S'))
        context['errors']      = reports.filter(status='E')
        
        return context  

# ==============================================================
#
# Administration Status View Use Information View
#
# ==============================================================

class AllUserInformationView(LoginRequiredMixin, FAENavigationMixin, TemplateView):
    template_name = 'accounts/all_user_information.html'

    def get_context_data(self, **kwargs):
        context = super(AllUserInformationView, self).get_context_data(**kwargs)

        user_profiles = UserProfile.objects.all()

        context['include_announcements']  = user_profiles.filter(email_announcements=True)
        context['exclude_announcements']  = user_profiles.filter(email_announcements=False)
        context['stats_users']             = StatsUser.objects.all()
        
        return context  


class UserInformationView(LoginRequiredMixin, FAENavigationMixin, TemplateView):
    template_name = 'accounts/user_information.html'

    def get_context_data(self, **kwargs):
        context = super(UserInformationView, self).get_context_data(**kwargs)

        user = User.objects.get(id=kwargs['user_id'])
        user_profile = UserProfile.objects.get(user=user)
        stats_user   = StatsUser.objects.get(user=user)

        context['user_profile'] = user_profile
        context['stats_user']   = stats_user
        
        return context  

