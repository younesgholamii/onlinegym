from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterationForm
from .models import User
from django.contrib import messages


class UserRegisterView(View):
    form_class = UserRegisterationForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'accounts/register.html', {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create(email=cd['email'], full_name=cd['full_name'])
            user.set_password(cd['password'])
            user.save()
            messages.success(request, 'registered successfully', 'success')
            return redirect('home:home')
        return render(request, 'accounts/register.html', {'form': form})
