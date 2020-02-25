from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
)
from django.contrib.auth import get_user_model

User = get_user_model()


class BlogUser(AbstractBaseUser):
    pass

class Additional(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'additional info'
        verbose_name_plural = 'additional infos'
