from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import CoachRegisterForm, CoachPostsForm, ExercisesForm, AppointmentAnswerForm
from accounts.models import User
from .models import Coach, CoachPosts, Appointment, Exercises, AppointmentAnswer, WorkoutPlan
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
            coach = get_object_or_404(Coach, user=request.user)
            post = CoachPosts.objects.create(coach=coach, title=cd['title'], content=cd['content'], image=cd['image'])
            post.save()
            messages.success(request, 'post created successfully', 'success')
            return redirect('home:home')
        return render(request, 'coaches/posts.html', {'form': form})


class UserAppointmentsView(LoginRequiredMixin, View):
    def get(self, request):
        appointments = Appointment.objects.filter(user__user__id=request.user.id).order_by('-created')
        return render(request, 'coaches/appointments.html', {'appointments': appointments})


class CoachesRequestView(LoginRequiredMixin, View):
    def get(self, request, coach_id):
        user = get_object_or_404(User, id=coach_id)
        requests = Appointment.objects.filter(coach__user__id=user.id)
        return render(request, 'coaches/requests.html', {'requests': requests})
        

class CoachesExercisesView(LoginRequiredMixin, View):
    def get(self, request, coach_id):
        user = get_object_or_404(User, id=coach_id)
        exercises = Exercises.objects.filter(coach__user__id=user.id)
        form = ExercisesForm()
        return render(request, 'coaches/exercises.html', {'exercises': exercises, 'form': form})
    
    def post(self, request, coach_id):
        form = ExercisesForm(request.POST)
        if form.is_valid():
            user = get_object_or_404(User, id=coach_id)
            coach = get_object_or_404(Coach, user__id=user.id)
            cd = form.cleaned_data
            exercise = Exercises.objects.create(coach=coach, name=cd['name'], category=cd['category'], sets=cd['sets'], reps=cd['reps'])
            exercise.save()
            messages.success(request, 'exercise added successfully', 'success')
            return redirect('coaches:coach_exercises', user.id)
        return render(request, 'coaches/exercises.html', {'form': form})


class CoachesAnswerView(LoginRequiredMixin, View):
    def get(self, request, appointment_id):
        form = AppointmentAnswerForm()
        exercises = Exercises.objects.filter(coach__user__id=request.user.id)
        appointment = get_object_or_404(Appointment, id=appointment_id)
        return render(request, 'coaches/answer.html', {'appointment': appointment, 'exercises': exercises, 'form': form})

    def post(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, id=appointment_id)
        form = AppointmentAnswerForm(request.POST)
        if form.is_valid():
            workout_plan, created = WorkoutPlan.objects.get_or_create(appointment=appointment)
            workout_plan.save()
            selected_exercises = form.cleaned_data['exercises']
            for exercise in selected_exercises:
                AppointmentAnswer.objects.create(
                    workout_plan=workout_plan,
                    name=exercise.name,
                    sets=exercise.sets,
                    reps=exercise.reps
                ).save()
            return redirect('coaches:coach_requests', request.user.id)
        return render(request, 'coaches/answer.html', {
        'appointment': appointment,
        'form': form,
        })

# class AddExerciseView(LoginRequiredMixin, View):

#     def get(self, request, appointment_id):
#         form = AppointmentAnswerForm()
#         return render(request, 'coaches/answer.html', {'form': form})

#     def post(self, request, appointment_id):
#         appointment = get_object_or_404(Appointment, id=appointment_id)
#         form = AppointmentAnswerForm(request.POST)
#         if form.is_valid():
#             workout_plan = WorkoutPlan.objects.create(appointment=appointment)

#             selected_exercises = form.cleaned_data['exercises']
#             for exercise in selected_exercises:
#                 Exercises.objects.create(
#                     workout_plan=workout_plan,
#                     name=exercise.name,
#                     sets=exercise.sets,
#                     reps=exercise.reps
#                 )
#             return redirect('coaches:coach_requests', request.user.id)
#         return render(request, 'coaches/answer.html', {
#         'appointment': appointment,
#         'form': form,
#         })