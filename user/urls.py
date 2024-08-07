from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', UserView.as_view(), name='signup'),
    path('signin/', UserLoginView.as_view(), name='login'),
]