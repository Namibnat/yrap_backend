from django.urls import path

from .views import  Routine

urlpatterns = [
    path('', Routine.as_view(), name='routine'),
]