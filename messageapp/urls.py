from django.urls import path
from .views import ChatView, GetChat, SendRequest, AcceptRequest

urlpatterns = [
    path("", ChatView.as_view(), name="login"),
    path("get_chat/<int:id>", GetChat.as_view(), name="get_chat"),
    path("send_request/", SendRequest.as_view(), name="send_request"),
    path("accept_request/", AcceptRequest.as_view(), name="accept_request")
    
]