from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import User, RegularUser

class UniqueFieldsValidationMixin:
    def clean_email(self):
        return self.validate_unique_field('email', 'this email has already exist.')

    def clean_phone_number(self):
        return self.validate_unique_field('phone_number', 'this phone number has already exist.')

    def clean_username(self):
        return self.validate_unique_field('username', 'this username has already exist.')

    def validate_unique_field(self, field_name, error_message):
        field_value = self.cleaned_data.get(field_name)
        if User.objects.filter(**{field_name: field_value}).exists():
            raise ValidationError(error_message)
        return field_value


class UserCreationForm(forms.ModelForm, UniqueFieldsValidationMixin):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'full_name']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("passwords are not the same")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user
    

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text='you can change password using <a href=\'../password/\'>this form</a>')

    class Meta:
        model = User
        fields = ['email', 'username', 'full_name', 'phone_number', 'password', 'image', 'is_active', 'is_admin']
        

class UserRegisterationForm(forms.Form, UniqueFieldsValidationMixin):
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=11)
    full_name = forms.CharField(max_length=50)
    username = forms.CharField(max_length=50)
    image = forms.ImageField(required=False, label="Image")
    password = forms.CharField(widget=forms.PasswordInput)


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserProfileEditForm(forms.ModelForm):
    height = forms.FloatField(required=False, label="height")
    weight = forms.FloatField(required=False, label="weight")
    
    class Meta:
        model = User
        fields = ['email', 'username', 'full_name', 'phone_number', 'date_of_birth', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self.instance, 'regular_profile'):
            self.fields['height'].initial = self.instance.regular_profile.height
            self.fields['weight'].initial = self.instance.regular_profile.weight

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            regular_user, created = RegularUser.objects.get_or_create(user=user)
            regular_user.height = self.cleaned_data['height']
            regular_user.weight = self.cleaned_data['weight']
            regular_user.save()
        return user