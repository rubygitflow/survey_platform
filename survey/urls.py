from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('polling/<int:queid>/', polling),
]
