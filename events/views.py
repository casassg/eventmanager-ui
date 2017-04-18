from django.views.generic import TemplateView

from django.shortcuts import render, redirect

# Create your views here.
from events import models


class EventListView(TemplateView):
    template_name = 'event-list.html'

    def get_context_data(self, **kwargs):
        return {'events': models.Events.objects.all()}

    def post(self,request, *args, **kwargs):



        return redirect('event_list')

