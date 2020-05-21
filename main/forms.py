from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User, Group

from .models import Comment, UserProfile, List


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
    password = forms.CharField(disabled=True)
    role = forms.ModelChoiceField(queryset=Group.objects.all(), widget=forms.Select())

    class Meta:
        model = User
        fields = ('email',
                  'first_name',
                  'last_name',
                  'password',
                  )

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            initial = kwargs.setdefault('initial', {})
            if kwargs['instance'].groups.all():
                initial['role'] = kwargs['instance'].groups.all()[0]
            else:
                initial['role'] = None
        forms.ModelForm.__init__(self, *args, **kwargs)

    def save(self):
        role = self.cleaned_data.pop('role')
        u = super().save()
        u.groups.set([role])

        return u


class ProfileForm(forms.ModelForm):
    role = forms.ModelChoiceField(queryset=Group.objects.all(), widget=forms.Select())

    class Meta:
        model = UserProfile
        fields = ('institute_name', 'registration_number', 'Address', 'phone', 'images', 'about')
        widgets = {
            'Address': forms.Textarea(attrs={'class': 'input'}),
            'about': forms.Textarea(attrs={'class': 'input', 'placeholders': 'Describe Yourself'}),
        }


class ListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ('name', 'description', 'image',
                  'noofdays', 'WhoIsConducting', 'category', 'daysLeft', 'slug', 'question')
        widgets = {
            'slug': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Replace by any text'}),
            'WhoIsConducting': forms.TextInput(
                attrs={'class': 'input', 'placeholder': 'The name of institution or company'}),
            'noofdays': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter the days left to register'}),

        }
