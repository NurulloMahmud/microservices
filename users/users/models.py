from django.db import models
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "users"


