from . import views
from django.urls import path

urlpatterns=[
    path('', views.home, name='home'),
    path('account/',views.account,name='account'),
    path('notification/',views.notification,name='notification'),
    path('account/login',views.login,name='login'),
    path('account/logout',views.logout)
]