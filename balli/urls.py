# everest_broker/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('report/', views.report, name='report'),
    path('userinput/', views.user_input, name='userinput'),
    path('timeline/', views.timeline, name='timeline'),
    path('notice/', views.notice, name='notice'),

]
