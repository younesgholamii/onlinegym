from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import UserRegisterationForm, UserLoginForm
from .models import User, RegularUser
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from coaches.forms import AppointmentForm
from coaches.models import Appointment, User, Coach


class UserRegisterView(View):
    form_class = UserRegisterationForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'accounts/register.html', {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create(email=cd['email'], username=cd['username'], full_name=cd['full_name'], phone_number=cd['phone_number'], image=cd['image'])
            user.set_password(cd['password'])
            user.save()
            RegularUser.objects.create(user=user)
            messages.success(request, 'registered successfully', 'success')
            return redirect('home:home')
        return render(request, 'accounts/register.html', {'form': form})


class UserLoginView(View):
    form_class = UserLoginForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Logged in successfully!', 'success')
                return redirect('home:home')
            else:
                messages.error(request, 'Invalid email or password', 'danger')
        return render(request, 'accounts/login.html', {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Logged out successfully!', 'success')
        return redirect('home:home')


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        coach = get_object_or_404(Coach, user=user)
        form = AppointmentForm()
        return render(request, 'accounts/profile.html', {'user': user, 'coach': coach, 'form': form})
    
    def post(self, request, user_id):
        form = AppointmentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = get_object_or_404(User, id=user_id)
            coach = get_object_or_404(Coach, user=user)
            appointment = Appointment.objects.create(
                user = get_object_or_404(RegularUser, user=request.user),
                coach = coach,
                first_name = cd['first_name'],
                last_name = cd['last_name'],
                phone_number = cd['phone_number'],
                age = cd['age'],
                weight = cd['weight'],
                height = cd['height'],
                plan = cd['plan'],
                descriptions = cd.get('descriptions', ''),
            )
            appointment.save()
            messages.success(request, 'Appointment sent successfully', 'success')
            return redirect('accounts:user_profile', user_id=user_id)