from django.urls import path
from accounts import views

urlpatterns = [
    path('auth/login', views.LoginView.as_view(), name='login'),
    path('auth/register', views.RegisterView.as_view(), name='register'),
    path('auth/logout', views.Logout.as_view(), name='logout'),
    path('profile/<int:id>/detail', views.Detail.as_view(), name='profile')
]