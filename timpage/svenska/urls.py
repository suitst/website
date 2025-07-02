from django.urls import path
from . import views

urlpatterns = [
    path("", views.game_start_view, name='game_start'),
    path("substantiv_game/", views.substantiv_game_view, name='substantiv_game'),
    path('substantiv_game/results/', views.substantiv_results_view, name='substantiv_results'),
    path('substantiv_game/next/', views.substantiv_next_question_view, name='next_question'),
    path('substantiv_game/summary/', views.substantiv_quit_view, name='substantiv_summary'),
]
