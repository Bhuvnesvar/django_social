"""dj_social URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/signup/', views.UserCreateAPIView),
    path('api/v1/login/', views.UserLoginAPIView),
    path('api/v1/users/', views.UserListAPIView),
    path('api/v1/user/search_user/', views.SearchUserAPIView),
    path('api/v1/user/send_friend_request/', views.SendFriendRequestAPIView),
    path('api/v1/user/accept_friend_request/', views.AcceptFriendRequestAPIView),
    path('api/v1/user/reject_friend_request/', views.RejectFriendRequestAPIView),
    path('api/v1/user/profile/', views.MyProfileAPIView),
]
