from django.shortcuts import render, redirect
from .models import Substantiv
import random

def substantiv_start_view(request):
    return render(request, 'substantiv_start.html')


def substantiv_game_view(request):
    categories = Substantiv.objects.values_list('category', flat=True).distinct()
    if request.method == 'POST':
        if 'Category' in request.POST:
            category = request.POST.get('Category')
            if category == 'all':
                words = Substantiv.objects.all()
            else:
                words = Substantiv.objects.filter(category=category)
            word = random.choice(words)
            request.session['current_word_num'] = word.number
            return render(request, 'substantiv_game.html', {'word': word, 'categories': categories})
    else:
        words = Substantiv.objects.all()
        word = random.choice(words)
        request.session['current_word_num'] = word.number
        return render(request, 'substantiv_game.html', {'word': word, 'categories': categories})


def substantiv_submit_view(request):
    if request.method == 'POST':
        word_number = request.session.get('current_word_num')
        word = Substantiv.objects.get(number=word_number)
        answers = {
            'engelska': request.POST.get('engelska'),
            'obestamt_singular': request.POST.get('obestamt_singular'),
            'bestamt_singular': request.POST.get('bestamt_singular'),
            'obestamt_plural': request.POST.get('obestamt_plural'),
            'bestamt_plural': request.POST.get('bestamt_plural'),
        }
        results = {
            'engelska_result': word.engelska == answers['engelska'],
            'obestamt_singular_result': word.obestämt_singular == answers['obestamt_singular'],
            'bestamt_singular_result': word.bestämt_singular == answers['bestamt_singular'],
            'obestamt_plural_result': word.obestämt_plural == answers['obestamt_plural'],
            'bestamt_plural_result': word.bestämt_plural == answers['bestamt_plural'],
        }
        return render(request, 'substantiv_results.html', {'word': word, 'answers': answers, 'results': results})
    

def next_question_view(request):
    return redirect('substantiv_game_view')


def quit_view(request):
    return render(request, 'substantiv_summary.html')