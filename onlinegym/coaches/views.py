from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import CoachRegisterForm, CoachPostsForm, ExercisesForm, AppointmentAnswerForm
from accounts.models import User
from .models import Coach, CoachPosts, Appointment, Exercises, AppointmentAnswer, WorkoutPlan
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AppointmentForm


class CoachRegisterView(View):
    """ coach register view """

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
    """ save posts in database """

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
    """ show all appointments that user reserved """

    def get(self, request):
        appointments = Appointment.objects.filter(user__user__id=request.user.id).order_by('-created')
        return render(request, 'coaches/appointments.html', {'appointments': appointments})


class UserAppointmentsDeleteView(LoginRequiredMixin, View):
    """ deleting the appointments """

    def get(self, request, appointment_id):
        get_object_or_404(Appointment, id=appointment_id).delete()
        messages.success(request, "appointment deleted successfully", 'success')
        return redirect('coaches:user_appointments')
    

class UserAppointmentsEditView(LoginRequiredMixin, View):
    """ editing the appointments """

    form_class = AppointmentForm
    def get(self, request, appointment_id):
        appointment =  get_object_or_404(Appointment, id=appointment_id, user=request.user.regular_profile)
        form = self.form_class(instance=appointment)
        return render(request, 'coaches/appointmentedit.html', {'form': form})
    
    def post(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user.regular_profile)
        form = self.form_class(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'appointment edited successfully', 'success')
            return redirect('coaches:user_appointments')
        return render(request, 'coaches/appointmentedit.html', {'form': form})



class CoachesRequestView(LoginRequiredMixin, View):
    """ show all requests for coaches """

    def get(self, request, coach_id):
        user = get_object_or_404(User, id=coach_id)
        appointments = Appointment.objects.filter(coach__user__id=user.id)
        return render(request, 'coaches/requests.html', {'appointments': appointments})
        

class CoachesExercisesView(LoginRequiredMixin, View):
    """ show and save all exercises """
    form_class = ExercisesForm

    def get(self, request, coach_id):
        user = get_object_or_404(User, id=coach_id)
        exercises = Exercises.objects.filter(coach__user__id=user.id)
        form = self.form_class()
        return render(request, 'coaches/exercises.html', {'exercises': exercises, 'form': form})
    
    def post(self, request, coach_id):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = get_object_or_404(User, id=coach_id)
            coach = get_object_or_404(Coach, user__id=user.id)
            cd = form.cleaned_data
            exercise = Exercises.objects.create(coach=coach, name=cd['name'], category=cd['category'], sets=cd['sets'], reps=cd['reps'])
            exercise.save()
            messages.success(request, 'exercise added successfully', 'success')
            return redirect('coaches:coach_exercises', user.id)
        return render(request, 'coaches/exercises.html', {'form': form})


class CoachesExercisesDeleteView(LoginRequiredMixin, View):
    def get(self, request, exercise_id, coach_id):
        get_object_or_404(Exercises, id=exercise_id).delete()
        messages.success(request, "exercise deleted successfully", "success")
        return redirect("coaches:coach_exercises", coach_id=coach_id)


class CoachesExercisesEditView(LoginRequiredMixin, View):
    form_class = ExercisesForm

    def get(self, request, exercise_id, coach_id):
        exercise = get_object_or_404(Exercises, id=exercise_id)
        form = self.form_class(instance=exercise)
        return render(request, 'coaches/exercisesedit.html', {'form': form})
    
    def post(self, request, exercise_id, coach_id):
        exercise = get_object_or_404(Exercises, id=exercise_id)
        form = self.form_class(request.POST, instance=exercise)
        if form.is_valid():
            form.save()
            messages.success(request, 'exercise edited successfully', 'success')
            return redirect('coaches:coach_exercises', coach_id=coach_id)
        return render(request, 'coaches/exercises.html', {'form': form})


class CoachesAnswerView(LoginRequiredMixin, View):
    """ save and send the answer of appointments to the users """

    form_class = AppointmentAnswerForm
    template_name = 'coaches/answer.html'

    def get(self, request, appointment_id):
        form = self.form_class(user=request.user)
        exercises = Exercises.objects.filter(coach__user=request.user)
        appointment = get_object_or_404(Appointment, id=appointment_id)
        return render(request, self.template_name, {
            'appointment': appointment,
            'exercises': exercises,
            'form': form
        })

    def post(self, request, appointment_id):
        form = self.form_class(request.POST, user=request.user)
        appointment = get_object_or_404(Appointment, id=appointment_id)
        
        if form.is_valid():
            cd = form.cleaned_data
            workout_plan, created = WorkoutPlan.objects.get_or_create(
                user=appointment.user,
                defaults={'name': cd['name']}
            )
            if not created:
                workout_plan.name = cd['name']
                workout_plan.save()
            
            for exercise in cd['exercises']:
                AppointmentAnswer.objects.create(
                    workout_plan=workout_plan,
                    exercise=exercise
                )
            appointment.workoutplan = workout_plan
            appointment.status = 'answered'
            appointment.save()
            return redirect('coaches:coach_requests', request.user.id)
        return render(request, self.template_name, {
            'appointment': appointment,
            'form': form,
            'exercises': Exercises.objects.filter(coach__user=request.user)
        })


class AppointmentAnswerView(LoginRequiredMixin, View):
    """ show the answer of requests to users """

    def get(self, request, appointment_id):
        appointment_answere = get_object_or_404(Appointment, id=appointment_id)
        appointment_answeres = AppointmentAnswer.objects.filter(workout_plan=appointment_answere.workoutplan)
        return render(request, 'coaches/seeplan.html', {'answeres': appointment_answeres})
