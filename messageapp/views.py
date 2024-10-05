import json
from django.shortcuts import render
from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from frontendapp.models import Useraccount, FriendRequest
from .models import Room
from django.db.models import Q
# Create your views here.

@method_decorator(login_required(login_url="/login/"), name="dispatch")
class ChatView(TemplateView,View):
    def get(self, request):
        # Get the Useraccount instance for the current user and prefetch friends
        current_user_account = Useraccount.objects.prefetch_related('friends').get(user=request.user)

        # Get the friends of the current user
        friends = current_user_account.friends.all()
       
        context = {
            'friends': friends,
        }
        return render(request, 'chat/chatpage.html', context)
    
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
    
@method_decorator(login_required(login_url="/login/"), name="dispatch")   
class SendRequest(View):
    def post(self, request):
        try:
            frm_usr = Useraccount.objects.get(user=request.user)
            to_usr = Useraccount.objects.get(user__username=request.POST.get('username'))
            pending_frm_request = FriendRequest.objects.filter(frm_usr=to_usr,to_usr=frm_usr).first()
            if pending_frm_request:
                return JsonResponse({"error":f"{to_usr.user.first_name} {to_usr.user.last_name}  is awaiting your acceptance of his friend request."},status=400)
            obj, created = FriendRequest.objects.get_or_create(frm_usr=frm_usr,to_usr=to_usr)
            return JsonResponse({"success":f"Your connection request has been send to {to_usr.user.first_name} {to_usr.user.last_name}"},status=201)
        except Useraccount.DoesNotExist:
            return JsonResponse({"error":"Oops....! Something Went Wrong"},status=404)
        
    def delete(self, request):
        try:
            data = json.loads(request.body)
            to_usr = data.get('username')
            type = data.get('type')
            print("++++++++++++++++++++++++++",type,":TYPE")
            frm_usr = Useraccount.objects.get(user=request.user)
            to_usr = Useraccount.objects.get(user__username=to_usr)
            print(frm_usr.user.first_name,"++++++++++++++++++++",to_usr.user.first_name)
            if type == "cancel":
                print("------------------////HERE")
                FriendRequest.objects.get(frm_usr=frm_usr,to_usr=to_usr).delete()
                return JsonResponse({"success":f"Friend request to {to_usr.user.first_name} {to_usr.user.last_name} has been canceled"},status=201)
            else:
                FriendRequest.objects.get(frm_usr=to_usr,to_usr=frm_usr).delete() 
                return JsonResponse({"success":f"Friend request from {to_usr.user.first_name} {to_usr.user.last_name} has been Rejected"},status=201)
        except FriendRequest.DoesNotExist:
            print("++++++HERE ERROR+++++++++++++")
            return JsonResponse({"error":"Oops....! Something Went Wrong"},status=404)
        
class AcceptRequest(View):
    def post(self, request):
        print(request.POST.dict(),"++++++++++++++++++++++++")
        try:
            frm_usr = Useraccount.objects.get(user=request.user)
            to_usr = Useraccount.objects.get(user__username=request.POST.get('username'))
            request_obj = FriendRequest.objects.get(frm_usr=to_usr,to_usr=frm_usr)
            request_obj.accept_status = True
            request_obj.save()
            frm_usr.friends.add(to_usr)
            to_usr.friends.add(frm_usr)
            return JsonResponse({"success":f"Now you can start conversations with {to_usr.user.first_name} {to_usr.user.last_name}"},status=200)
        except Exception as e:
            print(f"ERROR IN ACCEPT REQUEST:{e}")
            return JsonResponse({"error":"Oops....! Something Went Wrong"},status=404)