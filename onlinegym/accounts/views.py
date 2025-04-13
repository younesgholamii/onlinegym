from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import UserRegisterationForm, UserLoginForm, UserProfileEditForm
from .models import User, RegularUser
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from coaches.forms import AppointmentForm
from coaches.models import Appointment, User, Coach, RegularUser


class UserRegisterView(View):
    form_class = UserRegisterationForm
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
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
        return render(request, self.template_name, {'form': form})


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, "you logged in before", 'error')
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

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
        return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Logged out successfully!', 'success')
        return redirect('home:home')


class UserProfileView(LoginRequiredMixin, View):
    form_class = AppointmentForm
    template_name = 'accounts/profile.html'

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)            
        form = self.form_class()
        return render(request, self.template_name, {'user': user, 'form': form})
    
    def post(self, request, user_id):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            appointment = form.save(commit=False)
            user = get_object_or_404(RegularUser, user=request.user)
            coach_user = get_object_or_404(User, id=user_id)
            coach = get_object_or_404(Coach, user=coach_user)
            appointment.user = user
            appointment.coach = coach
            appointment.save()
            messages.success(request, 'Appointment sent successfully', 'success')
            return redirect('accounts:user_profile', user_id=user_id)
        return render(request, 'accounts/profile.html', {'form': form})
        

class UserProfileEditView(LoginRequiredMixin, View):
    form_class = UserProfileEditForm
    template_name = 'accounts/editprofile.html'

    def get(self, request):
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile editted successfully', 'success')
            return redirect('accounts:user_profile', user_id=request.user.id)
        return render(request, self.template_name, {'form': form})