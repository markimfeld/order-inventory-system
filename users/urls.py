from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    # path('profile-edit/', views.profile_edit, name='profile-edit'),
    # path('change-password/', views.change_password, name='change-password'),
]
