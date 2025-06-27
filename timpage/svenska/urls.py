from django.urls import path
from . import views

urlpatterns = [
    path("", views.svenska_substantiv, name='svenska_substantiv')
]
