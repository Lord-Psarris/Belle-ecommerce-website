from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, first_name=None, last_name=None, is_staff=False, is_active=True, is_admin=False):
        if not email:
            raise ValueError("All the fields haven't been adequately filled")
        if not password:
            raise ValueError("All the fields haven't been adequately filled - password")

        user_obj = self.model(
            email=self.normalize_email(email),
        )

        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.active = is_active
        user_obj.admin = is_admin
        user_obj.first_name = first_name
        user_obj.last_name = last_name
        user_obj.save(using=self._db)

        return user_obj

    def create_staffuser(self, email, password=None, first_name=None, last_name=None):
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, first_name='None', last_name='None'):
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


# Create your user models here.
class Users(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255, default='')

    # django defaults
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    # django default functions
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin
