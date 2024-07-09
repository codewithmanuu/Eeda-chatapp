from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Useraccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    profile_pic = models.FileField(upload_to="media/profile")
    friends = models.ManyToManyField('self',blank=True,null=True)
    def __str__(self):
        return self.user.first_name if self.user else "None"
    
class FriendRequest(models.Model):
    frm_usr = models.ForeignKey(Useraccount, related_name='frm_usr', on_delete=models.CASCADE, blank=True, null=True)
    to_usr = models.ForeignKey(Useraccount, related_name='to_usr',  on_delete=models.CASCADE, blank=True, null=True)
    accept_status = models.BooleanField(default=False,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return self.frm_usr.user.email + "  " + 'To' + "  " + self.to_usr.user.email
