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

from django.core.urlresolvers import reverse_lazy, reverse

from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView 
from django.views.generic import UpdateView 
from django.views.generic import TemplateView 
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.models import User

from .models import Contact

# Create your views here.
class ContactFormView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Contact
    fields = ['topic', 'message', 'status']
    template_name = 'contact/contact_form.html'

    success_url = reverse_lazy('contact_form')
    success_message = "Message on \"%(topic)s\" was sent succesfully sent"

    login_url = reverse_lazy('login')
    redirect_field_name = "Login"
    permission_denied_message = "You must login to contact the administrator"

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super(ContactFormView, self).form_valid(form)


# Create your views here.
class ResponseFormView(LoginRequiredMixin, UpdateView):
    model = Contact
    fields = ['topic', 'message', 'status', 'comments']
    template_name = 'contact/response_form.html'

    success_url = reverse_lazy('contacts')

    login_url = reverse_lazy('run_anonymous_report')
    redirect_field_name = "Anonymous Report"

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super(ResponseFormView, self).form_valid(form)

    def form_invalid(self, form):

        return super(ResponseFormView, self).form_invalid(form)  

class ResponsesView(LoginRequiredMixin, TemplateView):
    template_name = 'contact/responses.html'

    def get_context_data(self, **kwargs):
        context = super(ResponsesView, self).get_context_data(**kwargs)

        context['new_contacts']  = Contact.objects.filter(status='NR')
        context['old_contacts']  = Contact.objects.exclude(status='NR')
        
        return context            


