from django import forms
from django.contrib.auth.models import User
from .models import Post
from .models import UserProfile

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    
    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'first_name', 'last_name', 'email']
        
    def clean(self):
        cleaned_data = super().clean
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        # Check for validation of password
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Passwords do not match!')
        return self.cleaned_data


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'image']

class ProfileName(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name']
        
class ProfileImage(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profilePic']
        
class ProfileBio(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio']