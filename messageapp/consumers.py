import json
from django.db.models import Q
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from .models import Useraccount, Room, Messages

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
        print("==================//",event)

    def store_message(self,event):
        print("*******************>",event)
        data = json.loads(event)
        message = data['message']
        username = data['username']
        sender = Useraccount.objects.get(user__username=username)
        room = Room.objects.get(id=self.room.id)

        msg = Messages.objects.create(msg=message,sender=sender)
        room.meessages.add(msg)
        room.save()


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