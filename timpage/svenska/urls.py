from django.urls import path
from . import views

urlpatterns = [
    path("", views.substantiv_start_view, name='substantiv_start_view'),
    path("substantiv_game/", views.substantiv_game_view, name='substantiv_game_view'),
    path('substantiv_game/submit/', views.substantiv_submit_view, name='substantiv_submit_view'),
    path('substantiv_game/next/', views.next_question_view, name='next_question_view'),
    path('substantiv_game/summary/', views.quit_view, name='substantiv_summary'),
]
