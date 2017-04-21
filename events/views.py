from django.db import IntegrityError
from django.urls import reverse
from django.views.generic import TemplateView

from django.shortcuts import render, redirect

# Create your views here.
from kafka.errors import NoBrokersAvailable, UnknownTopicOrPartitionError

from events import models


class EventListView(TemplateView):
    template_name = 'event-list.html'

    def get_context_data(self, **kwargs):
        return {'events': models.Event.objects.all()}

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name', None)
        tokens = request.POST.get('tokens', None)
        try:
            models.Event.create(name, tokens)
        except IntegrityError:
            context = self.get_context_data()
            context.update({'errors': ['Event already exists with a similar name. Try a different name.', ]})
            return render(request, self.template_name, context, status=409)
        except NoBrokersAvailable:
            context = self.get_context_data()
            context.update({'errors': ['Kafka doesn\'t exist! No brokers available!', ]})
            return render(request, self.template_name, context, status=403)
        except UnknownTopicOrPartitionError:
            context = self.get_context_data()
            context.update({'errors': ['events topic doesn\'t exist!', ]})
            return render(request, self.template_name, context, status=403)
        return redirect('event_list')
