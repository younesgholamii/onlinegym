from django.urls import path
from .views import CoachRegisterView


app_name='coaches'
urlpatterns = [
    path('coachregister/', CoachRegisterView.as_view(), name='coach_register'),
]