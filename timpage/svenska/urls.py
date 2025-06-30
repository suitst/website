from django.urls import path
from . import views

urlpatterns = [
    path("", views.substantiv_start_view, name='substantiv_start'),
    path("substantiv_game/", views.substantiv_game_view, name='substantiv_game'),
    path('substantiv_game/results/', views.substantiv_results_view, name='substantiv_results'),
    path('substantiv_game/next/', views.next_question_view, name='next_question'),
    path('substantiv_game/summary/', views.quit_view, name='substantiv_summary'),
]
