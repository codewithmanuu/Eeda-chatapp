from django.urls import path
from .views import APIRegistrationView,APILoginView,APILogOutView,APIChatView


urlpatterns = [

    path('register/',APIRegistrationView.as_view(), name='register'),
    path('login/', APILoginView.as_view(), name='login'),
    path('logout/', APILogOutView.as_view(), name='logout'),
    path('chat/', APIChatView.as_view(), name='chat')
    
]