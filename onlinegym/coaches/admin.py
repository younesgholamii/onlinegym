from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Coach, CoachPosts, Appointment

admin.site.register(Coach)
admin.site.register(CoachPosts)
admin.site.register(Appointment)
