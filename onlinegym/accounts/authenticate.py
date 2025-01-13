from django.contrib.auth.backends import ModelBackend
from .models import User

class EmailOrUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(
                User.Q(email=username) | User.Q(username=username)
            )
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None
