from django.urls import path
from . import views

app_name = 'leagues'

urlpatterns = [
    path('', views.league_list, name='league_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('my-registrations/', views.my_registrations, name='my_registrations'),
    path('demo/', views.demo_leagues, name='demo_leagues'),
    path('demo/<int:index>/', views.demo_league_detail, name='demo_league_detail'),
    path('<int:pk>/', views.league_detail, name='league_detail'),
    path('<int:pk>/register/', views.register_for_league, name='register_for_league'),
    path('registration/<int:pk>/cancel/', views.cancel_registration, name='cancel_registration'),
]
