from django.shortcuts import render
from .models import User

# Create your views here.
def index(request):
    return render(request, "index.html", context={'users': User.objects.all()})