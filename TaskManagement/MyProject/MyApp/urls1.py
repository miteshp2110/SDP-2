from django.urls import path
from . import adminViews
urlpatterns = [
    path('',adminViews.home,name='adminHome'),
    path('accountAdmin/',adminViews.account,name='account'),
    path('accountAdmin/logout',adminViews.logout),
    path('accountAdmin/login',adminViews.login)

]