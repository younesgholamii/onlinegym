from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterationForm, UserLoginForm
from .models import User, RegularUser
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin


class UserRegisterView(LoginRequiredMixin, View):
    form_class = UserRegisterationForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'accounts/register.html', {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create(email=cd['email'], username=cd['username'], full_name=cd['full_name'], phone_number=cd['phone_number'])
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

