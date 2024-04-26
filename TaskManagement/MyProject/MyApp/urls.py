from . import views
from django.urls import path

urlpatterns=[
    path('', views.home, name='home'),
    path('createTask/', views.createTask, name='createTask'),
    path('myTasks/', views.myTasks, name='myTasks'),
    path('assignedTasks/', views.assignedTasks, name='assignedTasks'),
    path('notes/', views.notes, name='notes'),
    path('account/',views.account,name='account'),
    path('notification/',views.notification,name='notification'),
    path('account/login',views.login,name='login'),
    path('account/logout',views.logout),
    path('account/activeConnections',views.activeConnections),
    path('account/addConnections',views.addConnection),
    path('account/feedback', views.feedback, name='feedback'),
    path('account/processRequest',views.processRequest),
    path('notificationProcess/',views.acceptRequest),
    path('addTask/',views.addTask),
    path('readNotification/',views.clrNotification),
    path('deleteTask/',views.deleteTask),
    path('updateStatus/',views.updateStatus),
    path('addNotes/',views.addNotes),
    path('deleteNote/',views.deleteNote),
    path('updateDeadline/',views.updateDeadline),
    path('requestUpdate/',views.requestUpdate),
    path('deleteDeadline/',views.deleteDeadline)
]