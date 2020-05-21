from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('main/', include('main.urls')),
    path('account/create/', views.signupView, name='signup'),
    path('account/login/', views.signinView, name='signin'),
    path('account/logout/', views.signoutView, name='signout'),
    path('account/profile/', views.profileView, name='profile'),
    path('account/profile/edit/', views.editProfileView, name='editProfile'),
    path('account/profile/password/', views.changePassword, name='changePassword'),
    path('post/publish/', views.publish, name='publish'),
    path('list/register/', views.register, name='register')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
