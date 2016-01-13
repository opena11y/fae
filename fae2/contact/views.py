from django.core.urlresolvers import reverse_lazy, reverse

from django.views.generic import CreateView 
from django.views.generic import TemplateView 
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.models import User

from .models import Contact

# Create your views here.
class ContactFormView(LoginRequiredMixin, CreateView):
    model = Contact
    fields = ['topic', 'message', 'status']
    template_name = 'contact/contact_form.html'

    success_url = reverse_lazy('contacts')

    login_url = reverse_lazy('run_anonymous_report')
    redirect_field_name = "Anonymous Report"

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super(ContactFormView, self).form_valid(form)

    def form_invalid(self, form):

        return super(ContactFormView, self).form_invalid(form)


class ContactsView(LoginRequiredMixin, TemplateView):
    template_name = 'contact/contacts.html'

    def get_context_data(self, **kwargs):
        context = super(ContactsView, self).get_context_data(**kwargs)

        latest_contact = Contact.objects.filter(user=self.request.user).latest()
        all_contacts = Contact.objects.filter(user=self.request.user)

        context['last_contact'] = last_contact
        context['all_contacts'] = all_contacts
        
        return context   

# Create your views here.
class CommentsFormView(LoginRequiredMixin, CreateView):
    model = Contact
    fields = ['topic', 'message', 'status', 'comments', 'status']
    template_name = 'contact/contact_form.html'

    success_url = reverse_lazy('contacts')

    login_url = reverse_lazy('run_anonymous_report')
    redirect_field_name = "Anonymous Report"

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super(ContactFormView, self).form_valid(form)

    def form_invalid(self, form):

        return super(ContactFormView, self).form_invalid(form)        