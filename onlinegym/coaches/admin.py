from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Coach, CoachPosts, Appointment, Exercises, AppointmentAnswer, WorkoutPlan

admin.site.register(Coach)
admin.site.register(CoachPosts)
admin.site.register(Appointment)
admin.site.register(Exercises)
admin.site.register(AppointmentAnswer)
admin.site.register(WorkoutPlan)
