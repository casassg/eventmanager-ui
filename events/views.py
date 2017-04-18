from django.shortcuts import render


# Create your views here.


def get_events(request):
    render(request, 'event-list.html')
