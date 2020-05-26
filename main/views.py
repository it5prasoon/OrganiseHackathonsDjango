from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.urls import reverse

from .forms import SignUpForm, CommentForm, editProfileForm, ProfileForm, ListForm, SendEmail
from .models import Category, List, Comment


def index(request):
    return render(request, 'homepage.html')


def organiserView(request):
    return render(request, 'organiser.html')


# class Notification(TemplateView):
#     template_name = 'notifications.html'


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
        is_registered = False
        if list.register.filter(id=request.user.id).exists():
            is_registered = True
    except Exception as e:
        raise e
    return render(request, 'product.html',
                  {'list': list, 'is_registered': is_registered, 'total_registered': list.total_registered()})


def register(request):
    list = get_object_or_404(List, id=request.POST.get('list_id'))
    is_registered = False
    if list.register.filter(id=request.user.id).exists():
        list.register.remove(request.user)
        is_registered = False
    else:
        list.register.add(request.user)
        messages.success(request, "You are registered to the Event! Download the question!")
        is_registered = True
    return HttpResponseRedirect(list.get_url())


def addcomment(request, id):
    if request.method == 'POST':
        list = get_object_or_404(List, pk=id)
        form = CommentForm(request.POST or None)
        if form.is_valid():
            data = Comment()
            data.text = form.cleaned_data['text']
            print("Redirected.....")
            current_user = request.user
            data.user = current_user
            data.post = list
            data.user_id = current_user.id
            data.save()
            messages.success(request, "Your Comment has been sent. Thank you for your interest.")
            return HttpResponseRedirect(reverse('main:addcomment', args=[list.id]))
    else:
        form = CommentForm()

    return render(request, 'product.html', {'list': list, 'form': form})


def signupView(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            return redirect('signin')
    else:
        form = SignUpForm()
        profile_form = ProfileForm()

    return render(request, 'accounts/signup.html', {'form': form, 'profile_form': profile_form})


def editProfileView(request):
    if request.method == 'POST':
        form = editProfileForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.userprofile)

        if form.is_valid() and profile_form.is_valid():
            user_form = form.save()
            custom_form = profile_form.save(commit=False)
            custom_form.user = user_form
            custom_form.save()
            return redirect('profile')

    else:
        form = editProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.userprofile)
        args = {'form': form, 'profile_form': profile_form}
        return render(request, 'accounts/edit_profile.html', args)


def signinView(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
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


def publish(request):
    template = 'publish_list.html'
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.success(request, "You need to register as organiser first!")
            return redirect('signup')
        form = ListForm(request.POST or None, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, "Succesfully Published!")
            return redirect('main:allProdcat')
    else:
        form = ListForm()
    return render(request, template, {'list': list, 'form': form})


def send_email(request):
    if request.method == 'POST':
        form = SendEmail(request.POST, request.FILES)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = 'horg4dmin@yandex.com'
            email = form.cleaned_data['email']
            recipient = [email]
            send_mail(subject, message, from_email, recipient, fail_silently=True)
            HttpResponse("Mail Sent...")
    else:
        form = SendEmail()

    return render(request, 'send_email.html', {'form': form})