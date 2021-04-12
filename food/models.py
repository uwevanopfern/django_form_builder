from django.contrib.auth.models import User
from django.db import models
from forms_builder.forms.models import Form

# Create your models here.

class User(models.Model):
    forms = models.ManyToManyField(Form)
