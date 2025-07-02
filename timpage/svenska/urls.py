from django.urls import path
from . import views

urlpatterns = [
    path("", views.game_start_view, name='game_start'),
    path("substantiv_game/", views.substantiv_game_view, name='substantiv_game'),
    path('substantiv_game/results/', views.substantiv_results_view, name='substantiv_results'),
    path('substantiv_game/next/', views.substantiv_next_question_view, name='substantiv_next_question'),
    path('substantiv_game/summary/', views.substantiv_quit_view, name='substantiv_summary'),
    path("verb_game/", views.verb_game_view, name='verb_game'),
    path('verb_game/results/', views.verb_results_view, name='verb_results'),
    path('verb_game/next/', views.verb_next_question_view, name='verb_next_question'),
    path('verb_game/summary/', views.verb_quit_view, name='verb_summary'),
]
