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
    path('profile/', views.profile_detail, name='profile_detail'), # Profile [R]ead
    path('profile/edit/', views.profile_edit, name='profile_edit'), # Profile [U]pdate
    path('<str:username>/', views.profile, name='profile'),
]
