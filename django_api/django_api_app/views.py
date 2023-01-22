from django.shortcuts import render
from .models import KununuaUser

# Create your views here.
def index(request):
    return render(request, "index.html", context={'users': KununuaUser.objects.all()})