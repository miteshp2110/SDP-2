from . import views
from django.urls import path

urlpatterns=[
    path('', views.home, name='home'),
    path('account/',views.account,name='account'),
    path('notification/',views.notification,name='notification'),
    path('account/login',views.login,name='login'),
    path('account/logout',views.logout),
    path('account/activeConnections',views.activeConnections),
    path('account/addConnections',views.addConnection),
    path('account/feedback', views.feedback, name='feedback'),
    path('account/processRequest',views.processRequest),
    path('notificationProcess/',views.acceptRequest)
]