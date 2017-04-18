from django.db import IntegrityError
from django.urls import reverse
from django.views.generic import TemplateView

from django.shortcuts import render, redirect

# Create your views here.
from kafka.errors import NoBrokersAvailable

from events import models


class EventListView(TemplateView):
    template_name = 'event-list.html'

    def get_context_data(self, **kwargs):
        return {'events': models.Event.objects.all()}

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name', None)
        query = request.POST.get('query', None)
        try:
            models.Event.create(name, query)
        except IntegrityError:
            context = self.get_context_data()
            context.update({'errors': ['Event already exists with a similar name. Try a different name.', ]})
            return render(request, self.template_name, context, status=409)
        except NoBrokersAvailable:
            context = self.get_context_data()
            context.update({'errors': ['Kafka doesn\'t exist! No brokers available!', ]})
            return render(request, self.template_name, context, status=409)
        return redirect('event_list')
