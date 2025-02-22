from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone_number, email, full_name, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The phone number field must be set')
        if not email:
            raise ValueError('The email field must be set')
        if not full_name:
            raise ValueError('The full name field must be set')
        user = self.model(phone_number=phone_number, email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email, full_name, password=None, **extra_fields):
        user = self.create_user(phone_number=phone_number, email=email, full_name=full_name, password=password,
                                **extra_fields)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
