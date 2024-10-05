from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.views import View
from .forms import UserCreationForm,LoginForm
from rest_framework import status
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate
from django.contrib.auth import logout
from .models import Useraccount

class RegistrationView(TemplateView,View):
    form_class = UserCreationForm
    def get(self, request):
        if self.request.user.is_authenticated:
            return redirect('/chat/')
        return render(request, 'authentication/reg.html')

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            profile_pic = request.FILES.get('profile')
            Useraccount.objects.create(user=user, profile_pic=profile_pic)

            return JsonResponse({"success":"Account Created"}, status=201)
        else:
            return JsonResponse(form.errors, status=400)

class LoginView(TemplateView,View):
    form_class = LoginForm
    def get(self, request):
        if self.request.user.is_authenticated:
            return redirect('/chat/')
        return render(request, 'authentication/login.html')

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(email=form.cleaned_data.get("email"))
                username = str(user.username)
                password = form.cleaned_data.get("password")
                is_authenticated = authenticate(username=username,password=password,request=request)
                if is_authenticated:
                    login(request, is_authenticated)
                    return JsonResponse({"success":"Logged in"}, status=200)
                else:
                    return JsonResponse({"error":"Incorrect Email or Password"}, status=400)
            except Exception as e:
                return JsonResponse({"error":"Incorrect Email or Password"}, status=400)
        else:
            return JsonResponse(form.errors, status=200)
        



class LogOut(View):
    def get(self, request):
        logout(request)
        return redirect('/login/')