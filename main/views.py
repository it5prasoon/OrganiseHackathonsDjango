from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.urls import reverse

from .forms import SignUpForm, CommentForm
from .models import Category, List, Comment


def index(request):
    text_bar = 'A Event Organiser Specially for hackathons'
    return HttpResponse(text_bar)


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
                return redirect('main:allProdcat')
            else:
                return redirect('signup')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/signin.html', {'form': form})


def signoutView(request):
    logout(request)
    return redirect('signin')
