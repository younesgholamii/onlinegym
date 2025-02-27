from django.urls import path
from . import views


app_name='coaches'
urlpatterns = [
    path('coachregister/', views.CoachRegisterView.as_view(), name='coach_register'),
    path('coachpost/', views.CoachPostsView.as_view(), name='coach_post'),
    path('appointments/', views.UserAppointmentsView.as_view(), name='user_appointments'),
    path('requests/<int:coach_id>/', views.CoachesRequestView.as_view(), name='coach_requests'),
    path('exercises/<int:coach_id>/', views.CoachesExercisesView.as_view(), name='coach_exercises'),
    path('answer/<int:appointment_id>/', views.CoachesAnswerView.as_view(), name='coach_answer'),
    path('answer/add/<int:user_id>/<int:exercise_id>/', views.AddExerciseView.as_view(), name='coach_add_exercise'),
]