from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Coach

admin.site.register(Coach)
