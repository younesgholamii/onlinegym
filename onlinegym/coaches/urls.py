from django.urls import path
from .views import CoachRegisterView, CoachPostsView, UserAppointmentsView


app_name='coaches'
urlpatterns = [
    path('coachregister/', CoachRegisterView.as_view(), name='coach_register'),
    path('coachpost/', CoachPostsView.as_view(), name='coach_post'),
    path('appointments/', UserAppointmentsView.as_view(), name='user_appointments'),
]