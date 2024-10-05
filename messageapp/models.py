from django.db import models
from frontendapp.models import Useraccount, FriendRequest
# Create your models here.

class Messages(models.Model):
    msg = models.CharField(max_length=500000, blank=True, null=True)
    file = models.FileField(upload_to="media/messages", blank=True, null=True)
    sender = models.ForeignKey(Useraccount, on_delete=models.CASCADE,blank=True,null=True)

class Room(models.Model):
    frm = models.ForeignKey(Useraccount, related_name='frm', on_delete=models.CASCADE, blank=True, null=True)
    to = models.ForeignKey(Useraccount, related_name='to',  on_delete=models.CASCADE, blank=True, null=True)
    meessages = models.ManyToManyField(Messages,blank=True,null=True)
