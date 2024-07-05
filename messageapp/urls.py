from django.urls import path
from .views import ChatView, GetChat

urlpatterns = [
    path("", ChatView.as_view(), name="login"),
    path("get_chat/<int:id>", GetChat.as_view(), name="get_chat"),
    
]