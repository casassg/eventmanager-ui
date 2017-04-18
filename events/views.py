from django.shortcuts import render

# Create your views here.
from events import models


def get_events(request):
    return render(request, 'event-list.html', context={'events': models.Events.objects.all()})
