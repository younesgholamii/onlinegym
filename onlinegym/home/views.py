from django.shortcuts import render
from django.views import View
from coaches.models import CoachPosts


class HomeView(View):
    def get(self, request):
        posts = CoachPosts.objects.all()
        return render(request, 'home/home.html', {'posts': posts})
