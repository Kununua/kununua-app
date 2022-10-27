from django.urls import path, include
from . import views

app_name='django_api_app'
urlpatterns = [
    path('', views.index, name="index"),
]
