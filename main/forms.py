from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from .models import Comment, UserProfile


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('subject', 'text')

    widgets = {
        'subject': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Subject', 'cols': 100}),
        'text': forms.Textarea(attrs={'class': 'input', 'cols': 100})

    }


class editProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',
                  'first_name',
                  'last_name',
                  'password',
                  )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('institute_name', 'registration_number', 'Address', 'phone', 'images', 'about')
