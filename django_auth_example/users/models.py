from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    nickname = models.CharField(max_length=150,blank=True)
    email = models.EmailField(unique=True)

    class Meta(AbstractUser.Meta):
        pass

# class Profile(models.Model):
#     nickname = models.CharField(max_length=150,blank=True)
#     user = models.OneToOneField(User)