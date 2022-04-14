from django.urls import path
from . import views

app_name = 'shortener'
urlpatterns = [
    path('<str:pk>/', views.redirect_to, name='redirect'),
    path('<str:pk>/info', views.shortener_info, name='info'),
    path('', views.shortener_links, name='links'),
]
