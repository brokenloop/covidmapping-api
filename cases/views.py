import schedule
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import CoronaCaseRawSerializer
from .models import CoronaCaseRaw
from .updater import Updater

# is there a better place for this? 
updater = Updater()
updater.run()

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class CoronaCaseRawViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows raw corona cases to be viewed or edited.
    """
    queryset = CoronaCaseRaw.objects.all()
    serializer_class = CoronaCaseRawSerializer
    permission_classes = [permissions.IsAuthenticated]