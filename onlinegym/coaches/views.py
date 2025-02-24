from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import CoachRegisterForm, CoachPostsForm
from accounts.models import User
from .models import Coach, CoachPosts, Appointment
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


class CoachRegisterView(View):
    form_class = CoachRegisterForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'accounts/register.html', {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create(email=cd['email'], username=cd['username'], full_name=cd['full_name'], phone_number=cd['phone_number'], is_coach=True)
            user.set_password(cd['password'])
            user.save()
            Coach.objects.create(user=user, specialty=cd['specialty'], certifications=cd['certifications'])
            messages.success(request, 'registered successfully', 'success')
            return redirect('home:home')
        return render(request, 'accounts/register.html', {'form': form})


class CoachPostsView(LoginRequiredMixin, View):
    form_class = CoachPostsForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'coaches/posts.html', {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            post = CoachPosts.objects.create(coach=request.user, title=cd['title'], content=cd['content'], image=cd['image'])

            messages.success(request, 'post created successfully', 'success')
            return redirect('home:home')
        return render(request, 'coaches/posts.html', {'form': form})


class UserAppointmentsView(LoginRequiredMixin, View):
    def get(self, request):
        appointments = Appointment.objects.filter(user__user__id=request.user.id).order_by('-created')
        return render(request, 'coaches/appointments.html', {'appointments': appointments})


class CoachesRequestView(LoginRequiredMixin, View):
    def get(self, request, coach_id):
        user = User.objects.get(id=coach_id)
        requests = Appointment.objects.filter(coach__user__id=user.id)
        return render(request, 'coaches/requests.html', {'requests': requests})
        
