
from django.db import models
from forms_builder.forms.models import Form
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# Create your models here.

class UserManager(BaseUserManager):
    """ Helps django to work with our custom user model"""

    def create_new(self, email, username, password=None):
        """" Create a new user profile object  """

        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have a username')

        # normalize the email address by lower casing domain part of it
        # validate if email is in the standard format.
        email = self.normalize_email(email)
        user = self.model(email=email, username=username)

        # set_password encrypt our password
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password):
        """" Create a new super user with given details """

        user = self.create_new(email, username, password)

        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ User model"""

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    forms = models.ManyToManyField(Form)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        """ Used to convert django object into a string """
        return self.username
