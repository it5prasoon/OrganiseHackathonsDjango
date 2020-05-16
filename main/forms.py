from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    institute_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=254, help_text='eg. youremail@mail.com')
    registration_number = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'institute_name',
                  'registration_number')
