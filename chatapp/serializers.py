from .mixins import create_user_name
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['first_name','last_name','email','password','password2']
        extra_kwargs = {
            'password':{'write_only': True}
        }

    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        username = create_user_name()

        if password != password2:
            raise serializers.ValidationError({"error":"password does't match"})
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error':'Email already exists'})
        
        user = User(username=username,first_name=self.validated_data['first_name'],last_name=self.validated_data['last_name'],email=self.validated_data['email'])
        user.set_password(password)
        user.save()

        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type':'password'}, write_only=True)

    