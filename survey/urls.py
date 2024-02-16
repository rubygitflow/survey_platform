from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('polling/<int:queid>/', polling),
    path('poll/<int:polid>/question/<int:queid>/', poll),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('fraud/', fraud, name='fraud'),
    path('i18n/', include('django.conf.urls.i18n')),
]
