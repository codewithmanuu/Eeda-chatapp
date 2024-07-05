from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import RegistrationView,LoginView,LogOut

urlpatterns = [
    path("", RegistrationView.as_view()),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogOut.as_view(), name="logout"),
]