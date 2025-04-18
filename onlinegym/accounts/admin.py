from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, RegularUser
from .forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ['email', 'username', 'full_name', 'is_admin']
    list_filter = ['is_admin', 'username']
    fieldsets = [
        (None, {"fields": ["email", "username", 'full_name', 'phone_number', 'date_of_birth']}),
        ("Personal info", {"fields": ['image']}),
        ("Permissions", {"fields": ["is_admin", 'is_active']}),
    ]
    add_fieldsets = [
        (None, {'fields': ['email', 'full_name', 'password1', 'password2']}),
    ]
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = []


admin.site.register(User, UserAdmin)
admin.site.register(RegularUser)
admin.site.unregister(Group)
