from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>[^/]+)/$", consumers.ChatConsumer.as_asgi()),
    re_path(r"ws/friend_requests/", consumers.FriendsRequests.as_asgi()),
    re_path(r"ws/send_requests/", consumers.SendRequests.as_asgi()),
    re_path(r"ws/fetch_friends/", consumers.FriendConsumer.as_asgi()),
]