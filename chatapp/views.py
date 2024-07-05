from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import UserSerializer, LoginSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import logout

# Create your views here.

class APIRegistrationView(GenericAPIView):
    allowed_methods = ['POST']
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "Success": serializer.data,
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class APILoginView(GenericAPIView):
    allowed_methods = ['POST']
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(email=serializer.validated_data.get("email")).first()
            username = str(user.username)
            password = serializer.validated_data.get("password")
            is_authenticated = authenticate(username=username,password=password,request=request)
            if is_authenticated:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    "token": token.key
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error":"Incorrect Email or Password"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class APIChatView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        print(request.user)
        return render(request, 'frontendapp/templates/chatpage.html')

class APILogOutView(GenericAPIView):
    allowed_methods = ['POST']
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        print(request.user.username,"==============")
        request.user.auth_token.delete()
        logout(request)
        return Response({"success":"Success fully logged out"}, status=status.HTTP_200_OK)