from django.shortcuts import render
from django.views import View
from coaches.models import CoachPosts


class HomeView(View):
    def get(self, request):
        coach_username = request.GET.get('coach_username')

        if coach_username:
            posts = CoachPosts.objects.filter(coach__user__username__icontains=coach_username)
        else:
            posts = CoachPosts.objects.all()
        return render(request, 'home/home.html', {'posts': posts})
