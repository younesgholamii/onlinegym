from django.urls import path
from . import views


app_name='coaches'
urlpatterns = [
    path('coachregister/', views.CoachRegisterView.as_view(), name='coach_register'),
    path('coachpost/', views.CoachPostsView.as_view(), name='coach_post'),
    path('appointments/', views.UserAppointmentsView.as_view(), name='user_appointments'),
    path('appointments/delete/<int:appointment_id>/', views.UserAppointmentsDeleteView.as_view(), name='user_appointments_delete'),
    path('appointments/edit/<int:appointment_id>/', views.UserAppointmentsEditView.as_view(), name='user_appointments_edit'),
    path('requests/<int:coach_id>/', views.CoachesRequestView.as_view(), name='coach_requests'),
    path('exercises/<int:coach_id>/', views.CoachesExercisesView.as_view(), name='coach_exercises'),
    path('exercises/delete/<int:exercise_id>/<int:coach_id>/', views.CoachesExercisesDeleteView.as_view(), name='coach_exercises_delete'),
    path('exercises/edit/<int:exercise_id>/<int:coach_id>/', views.CoachesExercisesEditView.as_view(), name='coach_exercises_edit'),
    path('answer/<int:appointment_id>/', views.CoachesAnswerView.as_view(), name='coach_answer'),
    path('appointmentanswer/<int:appointment_id>/', views.AppointmentAnswerView.as_view(), name='appointment_answer'),
]