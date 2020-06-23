from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'), # User [C]reate
    path('login/', views.login, name='login'), # Session [C]reate
    path('logout/', views.logout, name='logout'), # Session [D]elete
    path('delete/', views.delete, name='delete'), # User [D]elete
    path('edit/', views.edit, name='edit'), # User [U]pdate
    path('password/', views.password, name='password'), # (Password) [U]pdate
]
