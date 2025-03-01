from django import forms
from accounts.models import User
from django.core.exceptions import ValidationError
from .models import Appointment, Exercises

class CoachRegisterForm(forms.Form):
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=11)
    full_name = forms.CharField(max_length=50)
    username = forms.CharField(max_length=50)
    specialty = forms.CharField(max_length=100)
    certifications = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('this email has already exists')
        return email
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        user = User.objects.filter(phone_number=phone_number).exists()
        if user:
            raise ValidationError('this phone_number has already exists')
        return phone_number
    
    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError('this username has already exists')
        return username
    


class CoachPostsForm(forms.Form):
    image = forms.ImageField(required=False, label="Image")
    title = forms.CharField(
        max_length=255,
        label="Title",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
    )
    content = forms.CharField(
        label="Content",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Enter content'}),
    )


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['first_name', 'last_name', 'phone_number', 'age', 'weight', 'height', 'plan', 'descriptions']


class ExercisesForm(forms.ModelForm):
    class Meta:
        model = Exercises
        fields = ['name', 'category', 'sets', 'reps']


class AppointmentAnswerForm(forms.Form):
    exercises = forms.ModelMultipleChoiceField(
        queryset=Exercises.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Select exercises'
    )
