from django.contrib import admin
from frontendapp.models import Useraccount,FriendRequest
from .models import Room,Messages
# Register your models here.
admin.site.register([Useraccount,Room,Messages,FriendRequest])