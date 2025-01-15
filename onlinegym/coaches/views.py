from django.shortcuts import render, redirect
from django.views import View
from .forms import CoachRegisterForm
from accounts.models import User
from .models import Coach
from django.contrib import messages


class CoachRegisterView(View):
    form_class = CoachRegisterForm

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
            Coach.objects.create(user=user, specialty=cd['specialty'], certifications=cd['certifications'])
            messages.success(request, 'registered successfully', 'success')
            return redirect('home:home')
        return render(request, 'accounts/register.html', {'form': form})


