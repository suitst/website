from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Substantiv
import random


@login_required
def game_start_view(request):
    categories = Substantiv.objects.values_list('category', flat=True).distinct()
    if request.method == 'POST':
        if 'game_stats' not in request.session:
                request.session['game_stats'] = {
                    'correct': {
                        'engelska': 0,
                        'obestamt_singular': 0,
                        'bestamt_singular': 0,
                        'obestamt_plural': 0,
                        'bestamt_plural': 0
                    },
                    'incorrect': {
                        'engelska': 0,
                        'obestamt_singular': 0,
                        'bestamt_singular': 0,
                        'obestamt_plural': 0,
                        'bestamt_plural': 0
                    }
                }
        return redirect('substantiv_game')
    return render(request, 'game_start.html', {'categories': categories})


@login_required
def substantiv_game_view(request):
    if request.method == 'POST':
        category = request.POST.get('category', request.session.get('category', 'all'))
        request.session['category'] = category
        print(category)
        if category == 'all':
            words = Substantiv.objects.all()
        else:
            words = Substantiv.objects.filter(category=category)
        word = random.choice(words)
        request.session['current_word_num'] = word.number
        return render(request, 'substantiv_game.html', {'word': word, 'category': category})
    else:
        return redirect('substantiv_game')


@login_required
def substantiv_results_view(request):
    if request.method == 'POST':
        user = request.user
        category = request.session.get('category')
        print(category)
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
        if 'game_stats' not in request.session:
            request.session['game_stats'] = {
                'correct': {field: 0 for field in ['engelska', 'obestamt_singular', 'bestamt_singular', 'obestamt_plural', 'bestamt_plural']},
                'incorrect': {field: 0 for field in ['engelska', 'obestamt_singular', 'bestamt_singular', 'obestamt_plural', 'bestamt_plural']}
            }
        
        user.update_total()

        for field, result in results.items():
            field_name = field.replace('_result', '')

            user.update_record(result, field)

            if result:
                request.session['game_stats']['correct'][field_name] += 1
            else:
                request.session['game_stats']['incorrect'][field_name] += 1
        
        user.save()
        
        request.session.modified = True
        print(request.session['game_stats'])
        return render(request, 'substantiv_results.html', {'word': word, 
                                                           'answers': answers, 
                                                           'results': results,
                                                           'game_stats': request.session['game_stats'], 
                                                           'category': category
                                                           })
    else:
        return redirect('substantiv_game')
    

@login_required
def next_question_view(request):
    if request.method == 'POST':
        # Retrieve the category from the POST data
        category = request.POST.get('category')

        # Store the category in the session to ensure it is retained
        request.session['category'] = category

        # Redirect to the game view
        return redirect('substantiv_game')

    # Redirect to the start page if the request method is not POST
    return redirect('game_start')


@login_required
def quit_view(request):
    game_stats = request.session.get('game_stats', {})

    # Clear the session data
    if 'game_stats' in request.session:
        del request.session['game_stats']

    # Calculate total attempts for each field
    totals = {}
    percentages = {'correct': {}, 'incorrect': {}}

    for field in game_stats['correct'].keys():
        correct = game_stats['correct'][field]
        incorrect = game_stats['incorrect'][field]
        totals[field] = correct + incorrect

        # Calculate percentage
        if totals[field] > 0:
            percentages['correct'][field] = (correct / totals[field]) * 100
            percentages['incorrect'][field] = (incorrect / totals[field]) * 100
        else:
            percentages['correct'][field] = 0
            percentages['incorrect'][field] = 0

    # Add totals and percentages to game_stats for use in the template
    game_stats['totals'] = totals
    game_stats['percentages'] = percentages

    return render(request, 'substantiv_summary.html', {'game_stats': game_stats})