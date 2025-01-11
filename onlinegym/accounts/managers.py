from django.contrib.auth.models import UserManager as BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, full_name, password):

        if not email:
            raise ValueError("user must have email")
        if not full_name:
            raise ValueError("user must have full name")
        if not password:
            raise ValueError("user must have password")
        
        user = self.model(email=self.normalize_email(email), full_name=full_name)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, full_name, password):

        user = self.create_user(email, full_name, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

