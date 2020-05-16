from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render

from .forms import SignUpForm
from .models import Category, List


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
                return redirect('store:allProdcat')
            else:
                return redirect('signup')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/signin.html', {'form': form})


def signoutView(request):
    logout(request)
    return redirect('signin')
