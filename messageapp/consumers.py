import json
import sys
from django.db.models import Q
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from .models import Useraccount, Room, Messages, FriendRequest
from django_redis import get_redis_connection
import traceback
import os

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        sender = self.scope['user']
        receiver = self.scope['url_route']['kwargs']['room_name']
        self.receiver_user = Useraccount.objects.get(user__username=receiver)
        self.sender_user = Useraccount.objects.get(user__username=sender)
        self.room = Room.objects.filter(
            Q(frm=self.sender_user, to=self.receiver_user) | Q(frm=self.receiver_user, to=self.sender_user)
        ).first()

        # If the room doesn't exist, create it
        if not self.room:
            self.room = Room.objects.create(frm=self.sender_user, to=self.receiver_user)
        self.room_name = f'personalchat_{self.room.id}'
        async_to_sync(self.channel_layer.group_add)(self.room_name,self.channel_name)
        self.accept()
        print("------------------->Web Socket Connected Successfully")
        for message in self.room.meessages.all():
            self.send(text_data=json.dumps({
                'message': message.msg if message else " ",
                'username': message.sender.user.username
            }))

        


    def websocket_disconnect(self,event):
        print(self.channel_name,"-----------------------------***-->","Websocket---Disconected")
        async_to_sync(self.channel_layer.group_discard)(self.room_name,self.channel_name)



    def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']

        self.store_message(text_data)

        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                'type': 'websocket.message',
                'message': message,
                'username': username
            }                                          
        
        )
        
    def websocket_message(self, event):
        message = event.get('message')
        username = event.get('username')
        
        # Send the message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    def store_message(self,event):
        data = json.loads(event)
        message = data['message']
        username = data['username']
        sender = Useraccount.objects.get(user__username=username)
        room = Room.objects.get(id=self.room.id)

        msg = Messages.objects.create(msg=message,sender=sender)
        room.meessages.add(msg)
        room.save()


class FriendsRequests(WebsocketConsumer):
    def connect(self):
        sender = self.scope['user']
        self.current_user = Useraccount.objects.get(user__username=sender)
        self.friend_requests = FriendRequest.objects.filter(to_usr=self.current_user,accept_status=False)
        count = len(self.friend_requests)
        self.room_name = f'friend_requests_{self.current_user.user.username}'
        async_to_sync(self.channel_layer.group_add)(self.room_name,self.channel_name)
        self.accept()

        # Add room name to active rooms in Redis
        redis_conn = get_redis_connection("default")
        redis_conn.sadd("active_rooms", self.room_name)

        print("FriendsRequests+++++++++CONNECTED SUCCESSFULLY+++++++++",self.channel_name,f"ROOM NAME:{self.room_name}")
        if self.friend_requests:
            for friends in self.friend_requests:
                profile_pic_url = friends.frm_usr.profile_pic.url if friends.to_usr.profile_pic else None
                self.send(text_data=json.dumps({
                    'username': friends.frm_usr.user.username,
                    'first_name': friends.frm_usr.user.first_name,
                    'last_name': friends.frm_usr.user.last_name,
                    'profile_pic': profile_pic_url,
                    'count': count,
                }))
        else:
            self.send(text_data=json.dumps({
                'no_friends': True,
            }))

    def websocket_disconnect(self,event):
        print(self.channel_name,"FriendsRequests-----------------------------***-->","Websocket---Disconected",f"ROOM NAME:{self.room_name}")
        
        # Remove room name from active rooms in Redis
        redis_conn = get_redis_connection("default")
        redis_conn.srem("active_rooms", self.room_name)

        async_to_sync(self.channel_layer.group_discard)(self.room_name,self.channel_name)

    def receive(self, text_data):
        try:
            data = json.loads(text_data)
            to_username = data['to_username']
            type = data.get('type')
            sender = self.scope['user']
            self.user = Useraccount.objects.get(user__username=sender)
            self.to_user = Useraccount.objects.get(user__username=to_username)
            requests = FriendRequest.objects.filter(to_usr=self.to_user,accept_status=False)
            count = len(requests)
            latest_friend_request = FriendRequest.objects.filter(frm_usr=self.user,to_usr=self.to_user,accept_status=False).order_by('-created_at').first()
            to_room_name = f'friend_requests_{self.to_user.user.username}'
            if not type:
                if latest_friend_request and self.room_exists(to_room_name):
                    profile_pic_url = latest_friend_request.frm_usr.profile_pic.url if latest_friend_request.frm_usr.profile_pic else None
                    async_to_sync(self.channel_layer.group_send)(
                        to_room_name,
                        {
                            'type': 'websocket.message',
                            'username': latest_friend_request.frm_usr.user.username,
                            'first_name': latest_friend_request.frm_usr.user.first_name,
                            'last_name': latest_friend_request.frm_usr.user.last_name,
                            'profile_pic': profile_pic_url,
                            'cancel' : False,
                            'count': count,
                        }
                    )
            else:
               async_to_sync(self.channel_layer.group_send)(
                    to_room_name,
                    {
                        'type': 'websocket.remove_message',
                        'username': self.user.user.username,
                        'cancel': True,
                        'count': count,
                    }
                ) 
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            line_number = exc_tb.tb_lineno
            function_name = exc_tb.tb_frame.f_code.co_name
            print(f"{e} *******************ERROR")
            print(f"Exception occurred in file: {fname}")
            print(f"Function name: {function_name}")
            print(f"Line number: {line_number}")
            traceback.print_exc()
    
    def websocket_message(self, event):
        username = event.get('username')
        first_name = event.get('first_name')
        last_name = event.get('last_name')
        profile_pic = event.get('profile_pic')
        cancel = event.get('cancel')
        count = event.get('count')
        
        # Send the message to WebSocket
        self.send(text_data=json.dumps({
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'profile_pic': profile_pic,
            'cancel': cancel,
            'count': count,
        }))

    def websocket_remove_message(self, event):
        username = event.get('username')
        cancel = event.get('cancel')
        
        # Send the message to WebSocket
        self.send(text_data=json.dumps({
            'username': username,
            'cancel': cancel,
        }))

    def room_exists(self, room_name):
        redis_conn = get_redis_connection("default")
        active_rooms = redis_conn.smembers("active_rooms")

        # for room in active_rooms:
        #     print(room.decode('utf-8'),"FriendsRequests============================ACTIVE ROOMS")

        return redis_conn.sismember("active_rooms", room_name)
    

class SendRequests(WebsocketConsumer):
    def connect(self):
        sender = self.scope['user']
        self.current_user = Useraccount.objects.get(user__username=sender)
        users = Useraccount.objects.filter(~Q(user__username=sender),user__is_staff=False)
        # Get the Useraccount instance for the current user and prefetch friends
        current_user_account = Useraccount.objects.prefetch_related('friends').get(user__username=sender)

        # Get the friends of the current user
        friends_ids = current_user_account.friends.values_list('id', flat=True)

        # Get users involved in friend requests with the current user (both sent and received)
        friend_requests_received = FriendRequest.objects.filter(to_usr=current_user_account).values_list('frm_usr_id', flat=True)
        friend_requests_send = FriendRequest.objects.filter(frm_usr=current_user_account).values_list('to_usr_id', flat=True)

        # Combine the friends and friend request user IDs into a single list
        exclude_ids = set(friends_ids).union(friend_requests_received)

        # Get all users except the current user, their friends, and those involved in friend requests
        users_not_friends = Useraccount.objects.exclude(
            user__username=sender
        ).exclude(
            id__in=exclude_ids
        )
        self.room_name = f'send_requests_{self.current_user.user.username}'
        async_to_sync(self.channel_layer.group_add)(self.room_name,self.channel_name)
        self.accept()

        # Add room name to active rooms in Redis
        redis_conn = get_redis_connection("default")
        redis_conn.sadd("send_active_rooms", self.room_name)

        print("SendRequests+++++++++CONNECTED SUCCESSFULLY+++++++++",self.channel_name,f"ROOM NAME:{self.room_name}")
        for users in users_not_friends:
            profile_pic_url = users.profile_pic.url if users.profile_pic else None
            self.send(text_data=json.dumps({
                'username': users.user.username,
                'first_name': users.user.first_name,
                'last_name': users.user.last_name,
                'profile_pic': profile_pic_url,
                'is_sended' : True if users.id in friend_requests_send else False
            }))

    def websocket_disconnect(self,event):
        print(self.channel_name,"SendRequests-----------------------------***-->","Websocket---Disconected",f"ROOM NAME:{self.room_name}")
        
        # Remove room name from active rooms in Redis
        redis_conn = get_redis_connection("default")
        redis_conn.srem("send_active_rooms", self.room_name)

        async_to_sync(self.channel_layer.group_discard)(self.room_name,self.channel_name)

    def receive(self, text_data):
        try:
            print("SendRequests -- HERE HERE++++++++++++++++++++")
            data = json.loads(text_data)
            to_username = data['to_username']
            self.types = data.get('type')
            sender = self.scope['user']
            self.user = Useraccount.objects.get(user__username=sender)
            self.to_user = Useraccount.objects.get(user__username=to_username)
            to_room_name = f'send_requests_{self.to_user.user.username}'
            if self.types == 'accepted':
                if self.room_exists(to_room_name):
                    async_to_sync(self.channel_layer.group_send)(
                        to_room_name,
                        {
                            'type': 'websocket.message',
                            'username': self.user.user.username,
                            'is_accepted': True,
                        }
                    )
            else:
               if self.room_exists(to_room_name):
                    async_to_sync(self.channel_layer.group_send)(
                        to_room_name,
                        {
                            'type': 'websocket.remove_message',
                            'username': self.user.user.username,
                            'is_rejected': True,
                        }
                    ) 
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            line_number = exc_tb.tb_lineno
            function_name = exc_tb.tb_frame.f_code.co_name
            print(f"{e} *******************ERROR")
            print(f"Exception occurred in file: {fname}")
            print(f"Function name: {function_name}")
            print(f"Line number: {line_number}")
            traceback.print_exc()
    
    def websocket_message(self, event):
            username = event.get('username')
            is_accepted = event.get('is_accepted')
            self.send(text_data=json.dumps({
                'username': username,
                'is_accepted': is_accepted,
            }))


    def websocket_remove_message(self, event):
            username = event.get('username')
            is_rejected = event.get('is_rejected')
            self.send(text_data=json.dumps({
                'username': username,
                'is_rejected': is_rejected,
            }))
        

    def room_exists(self, room_name):
        redis_conn = get_redis_connection("default")
        # active_rooms = redis_conn.smembers("send_active_rooms")

        # for room in active_rooms:
        #     print(room.decode('utf-8'),"SendRequests============================ACTIVE ROOMS")

        return redis_conn.sismember("send_active_rooms", room_name)
        

""" Currently i'm fetching all my friends using webscoket because if need any updation in feature we can update on this """
class FriendConsumer(WebsocketConsumer):
    def connect(self):
        sender = self.scope['user']
        current_user_account = Useraccount.objects.prefetch_related('friends').get(user__username=sender)

        # Get the friends of the current user
        friends = current_user_account.friends.all()

        # If the room doesn't exist, create it
        self.room_name = f'{sender}_friends'
        async_to_sync(self.channel_layer.group_add)(self.room_name,self.channel_name)
        self.accept()
        print("------------------->Web Socket Connected Successfully")
        if friends.exists():
            for friend in friends:
                profile_pic_url =friend.profile_pic.url if friend.profile_pic.url else None
                self.send(text_data=json.dumps({
                    'id': friend.user.id,
                    'username': friend.user.username,
                    'first_name': friend.user.first_name,
                    'last_name': friend.user.last_name,
                    'profile_pic': profile_pic_url,
                }))
        else:
            self.send(text_data=json.dumps({
                'no_friends': True,
            }))
    def websocket_disconnect(self,event):
        print(self.channel_name,"FriendConsumer-----------------------------***-->","Websocket---Disconected",f"ROOM NAME:{self.room_name}")

        async_to_sync(self.channel_layer.group_discard)(self.room_name,self.channel_name)

    # async def chat_message(self, event):
    #     message = event['message']
    #     username = event['username']

    #     await self.send(text_data=json.dumps({
    #         'message': message,
    #         'username': username
    #     }))

# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()
#         self.send(text_data=json.dumps({"message": "websocket connected successfully"}))

#     def disconnect(self, close_code):
#         pass

#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]

#         self.send(text_data=json.dumps({"message": message}))