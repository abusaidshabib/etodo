from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
