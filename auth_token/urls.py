from django.conf.urls import url
from django.urls import path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = [
    # url(r'^register/', views.register, name='user-register'),
    path('register-user/', views.register, name='user-register'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

auth_router = routers.DefaultRouter()
auth_router.register(r'users', views.UserViewSet)