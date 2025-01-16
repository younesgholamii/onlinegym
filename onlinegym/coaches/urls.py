from django.urls import path
from .views import CoachRegisterView, CoachPostsView


app_name='coaches'
urlpatterns = [
    path('coachregister/', CoachRegisterView.as_view(), name='coach_register'),
    path('coachpost/', CoachPostsView.as_view(), name='coach_post'),
]