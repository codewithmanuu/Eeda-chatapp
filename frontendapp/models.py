from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Useraccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    profile_pic = models.FileField(upload_to="media/profile")

    def __str__(self):
        return self.user.first_name if self.user else "None"
