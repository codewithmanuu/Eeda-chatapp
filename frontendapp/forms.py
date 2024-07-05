from django import forms
from django.contrib.auth.models import User
from chatapp.mixins import create_user_name

class UserCreationForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['first_name','last_name','email','password','password2']
        extra_kwargs = {
            'password':{'write_only': True}
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        email = cleaned_data.get('email')
        print(email,"------------------------------")

        if password and password2 and password != password2:
            self.add_error('password2', "Passwords don't match")

        if User.objects.filter(email=email).exists():
            self.add_error('email', 'Email already exists')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = create_user_name()
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())