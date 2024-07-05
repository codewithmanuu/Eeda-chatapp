from django.contrib import admin
from frontendapp.models import Useraccount
from .models import Room,Messages
# Register your models here.
admin.site.register([Useraccount,Room,Messages])