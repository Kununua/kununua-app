from django.urls import path
from . import views

app_name = "scraper"
urlpatterns = [
    path('matchingTraining/', views.matching_training_view, name='matching_training'),
]

