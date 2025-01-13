from django.contrib.auth.models import UserManager as BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, username, full_name, phone_number, password, **kwargs):

        if not email:
            raise ValueError("user must have email")
        if not username:
            raise ValueError("user must have username")
        if not password:
            raise ValueError("user must have password")
        if not full_name:
            raise ValueError("user must have full name")
        if not phone_number:
            raise ValueError("user must have phone number")
        
        user = self.model(email=self.normalize_email(email), username=username, full_name=full_name, phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, full_name, phone_number, password, **kwargs):
        user = self.create_user(email, username, full_name, phone_number, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

