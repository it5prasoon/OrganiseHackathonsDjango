from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.allProdcat, name='allProdcat'),
    path('<slug:c_slug>/', views.allProdcat, name='hackathonCategory'),
    path('<slug:c_slug>/<slug:product_slug>/', views.hackathonList, name='hackathonList'),
    path('addcomment/<int:id>', views.addcomment, name='addcomment'),
]
