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

file: accounts/views.py

Author: Jon Gunderson

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


from django.contrib.auth.models  import User
from userProfiles.models         import UserProfile
from accounts.models             import AccountType
from stats.models                import StatsUser
from websiteResultGroups.models  import WebsiteReportGroup

from subscriptions.models        import Payment


from django.forms.models import inlineformset_factory


from django import forms


from websiteResults.models import WebsiteReport

import datetime

from timezone_field import TimeZoneFormField

from reports.views import FAENavigationMixin

from fae2.settings import SITE_URL
from fae2.settings import SHIBBOLETH_SUPERUSER

from userProfiles.models import UserProfile
from stats.models        import StatsUser


def getExpirationDate(dt, months):

    if (not dt):
      dt = datetime.datetime.now()

    year  = dt.year
    month = dt.month + months
    day   = dt.day

    if day > 28:
        day = 1
        month += 1

    if month > 12:
        month = 1
        year += 1

    return 


# Create your views here.


class HeaderInfo(LoginRequiredMixin, TemplateView):
   template_name = 'registration/header_info.html'


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
            atype = AccountType.objects.get(type_id=1)
            profile = UserProfile(user=user, account_type=atype)
            profile.save()

        try: 
            stats = StatsUser.objects.get(user=user)
        except ObjectDoesNotExist:
            wsrg =  WebsiteReportGroup(title="Summary of results for " + str(user))
            wsrg.save()
            stats = StatsUser(user=user, ws_report_group=wsrg)  
            stats.save()

        # Try to populate user information from shibboleth information
        if user.first_name == '' or user.last_name == '' or user.email == '':
            try:
                user.first_name = self.request.META['givenName']
                user.last_name  = self.request.META['sn']
                user.email      = self.request.META['mail']
                user.save()
            except:
                pass    

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


class AccountTypeForm(forms.Form):
    account_type        = forms.CharField(max_length=3)
    payment_duration    = forms.CharField(max_length=3)
    payment_amount      = forms.CharField(max_length=20)


class UpdateAccountTypeView(LoginRequiredMixin, FAENavigationMixin, SuccessMessageMixin, FormView):
    template_name = 'accounts/update_account_type.html'
    form_class    = AccountTypeForm

    success_url = reverse_lazy('update_account_type')
    success_message = "Account Type Updated!"

    login_url = reverse_lazy('run_anonymous_report')
    redirect_field_name = "Anonymous Report"

    updated = False
    errors  = False

    def form_valid(self, form):

        user = self.request.user

        account_type      = form.cleaned_data['account_type']
        payment_duration  = form.cleaned_data['payment_duration']
        amount            = form.cleaned_data['payment_amount']

        profile           = user.profile
        profile.account_type    = AccountType.objects.get(id=account_type)
#        profile.expiration_date = datetime.datetime.now()
        profile.save()

        return super(UpdateAccountTypeView, self).form_valid(form)
  

    def get_initial(self):
        # Populate ticks in BooleanFields
        user = self.request.user
        initial = {}
        initial['account_type'] = self.request.user.profile.account_type.type_id
        return initial

    def get_context_data(self, **kwargs):
        context = super(UpdateAccountTypeView, self).get_context_data(**kwargs)

        context['user_stats']    = StatsUser.objects.get(user=self.request.user)
        context['user_profile']  = UserProfile.objects.get(user=self.request.user)
        context['account_types'] = AccountType.objects.filter(self_registration=True)
        
        return context  



# ==============================================================
#
# Donation Views
#
# ==============================================================

class DonateForm(forms.Form):
    donor_name           = forms.CharField(max_length=40)
    donor_email          = forms.EmailField(max_length=60)
    donation_amount      = forms.IntegerField()
    show_donation        = forms.BooleanField(required=False    )


class DonateView(FAENavigationMixin, SuccessMessageMixin, FormView):
    template_name = 'accounts/donate.html'
    form_class    = DonateForm

    success_url = reverse_lazy('donate_success')
    success_message = "Thank you for your support!"

    def form_valid(self, form):

        print("USER 1: " + str(self.request.user))    

        user = self.request.user

        if user.is_anonymous():
            user = User.objects.get(username='anonymous')    

        print("USER 2: " + str(user))    

        name           = form.cleaned_data['donor_name']
        email          = form.cleaned_data['donor_email']
        amount         = form.cleaned_data['donation_amount']
        show_donation  = form.cleaned_data['show_donation']

        payment = Payment(user=user, name=name, email=email, amount=amount, show_donation=show_donation)
        payment.save()

        return super(DonateView, self).form_valid(form) 

    def get_initial(self):
        # Populate ticks in BooleanFields
        initial = {}

        initial['donor_name']  = ''
        initial['donor_email'] = ''
        initial['show_donation']   = False

        if not self.request.user.is_anonymous():
            user = self.request.user
            initial['donor_name']  = user.first_name + ' ' + user.last_name
            initial['donor_email'] = user.email
            initial['show_donation']   = True

        return initial        


class DonateSuccessView(FAENavigationMixin, TemplateView):
    template_name = 'accounts/donate_success.html'

    def get_context_data(self, **kwargs):
        context = super(DonateSuccessView, self).get_context_data(**kwargs)

        
        return context  

class DonateFailView(FAENavigationMixin, TemplateView):
    template_name = 'accounts/donate_fail.html'

    def get_context_data(self, **kwargs):
        context = super(DonateFailView, self).get_context_data(**kwargs)

        return context  


# ==============================================================
#
# Administrator Views
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

