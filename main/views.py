from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.urls import reverse

from .forms import SignUpForm, CommentForm, editProfileForm, ProfileForm
from .models import Category, List, Comment


def index(request):
    return render(request, 'homepage.html')


def allProdcat(request, c_slug=None):
    c_page = None
    lists = None
    if c_slug != None:
        c_page = get_object_or_404(Category, slug=c_slug)
        lists = List.objects.filter(category=c_page, daysLeft=True)
    else:
        lists = List.objects.all().filter(daysLeft=True)
    return render(request, 'category.html', {'category': c_page, 'lists': lists})


def hackathonList(request, c_slug, product_slug):
    try:
        list = List.objects.get(category__slug=c_slug, slug=product_slug)
    except Exception as e:
        raise e
    return render(request, 'product.html', {'list': list})


def addcomment(request, id):
    list = get_object_or_404(List, pk=id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        data = Comment()
        data.subject = form.cleaned_data['subject']
        data.text = form.cleaned_data['text']
        print("Redirected.....")
        current_user = request.user
        data.user = current_user
        data.post = list
        data.user_id = current_user.id
        data.save()
        messages.success(request, "Your Comment has been sent. Thank you for your interest.")
        return HttpResponseRedirect(reverse('main:addcomment', args=[list.id]))
    return render(request, 'product.html', {'list': list, 'form': form})


def signupView(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            signup_user = User.objects.get(username=username)
            # customer_group = Group.objects.get(name='Customer')
            # customer_group.user_set.add(signup_user)
            return redirect('signin')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def signinView(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return redirect('signup')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/signin.html', {'form': form})


def profileView(request):
    args = {'user': request.user}
    return render(request, 'accounts/profile.html', args)


def signoutView(request):
    logout(request)
    return redirect('signin')


def editProfileView(request):
    if request.method == 'POST':
        form = editProfileForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.userprofile)

        if form.is_valid() and profile_form.is_valid():
            user_form = form.save()
            custom_form = profile_form.save(False)
            custom_form.user = user_form
            custom_form.save()
            return redirect('profile')

    else:
        form = editProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.userprofile)
        args = {'form': form, 'profile_form': profile_form}
        return render(request, 'accounts/edit_profile.html', args)


def changePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('profile')
        else:
            return redirect('changePassword')
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'accounts/changePassword.html', args)
