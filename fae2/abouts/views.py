from django.http import HttpResponse
from django.views.generic import TemplateView

class Overview(TemplateView):
    template_name = 'abouts/overview.html'
