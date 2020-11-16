from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'recommender-home'),
    path('about/', views.about, name = 'recommender-about'),
    path('userEntered/<name>/', views.userEntered, name = 'entered-user'),
    path('follow/', views.follow, name = 'user-follow'),
]