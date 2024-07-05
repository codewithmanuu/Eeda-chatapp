from django.shortcuts import render
from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from frontendapp.models import Useraccount
from .models import Room
from django.db.models import Q
# Create your views here.

@method_decorator(login_required(login_url="/login/"), name="dispatch")
class ChatView(TemplateView,View):
    template_name = 'chat/chatpage.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = Useraccount.objects.filter(~Q(user__username=self.request.user),user__is_staff=False)
        context = {'users': users}
        return context
    
@method_decorator(login_required(login_url="/login/"), name="dispatch")   
class GetChat(View):
    def get(self, request, id):
        context = {}
        try:
            to_user = Useraccount.objects.get(user_id=id)
            frm_user = Useraccount.objects.get(user=request.user)
            room = Room.objects.get(frm=frm_user, to=to_user)
            messages = room.meessages.all()
            message_list = [{'content': msg.msg, 'sender': msg.sender.user.username} for msg in messages]
            context['messages'] = message_list
        except Room.DoesNotExist:
            print("++++++++++++++++++++++++++")
            context['messages'] = []
        context['user'] = {'first_name': to_user.user.first_name, 'last_name': to_user.user.last_name}
        return JsonResponse(context, status=200)