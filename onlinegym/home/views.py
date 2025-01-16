from django.shortcuts import render
from django.views import View
from accounts.models import User


class HomeView(View):
    def get(self, request):
        coaches = User.objects.filter(is_coach=True)
        return render(request, 'home/home.html', {'coaches': coaches})
