from django.http import HttpResponse
from django.views.generic import View

class RunReport(View):
    def get(self, request):
        # <view logic>
        return HttpResponse('run report')

