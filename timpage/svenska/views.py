from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Substantiv, Verb
import random
import unicodedata


def ensure_game_stats(request, required_fields):
    """
    Ensure request.session['game_stats'] exists and has zeroed counters
    for all required_fields under both 'correct' and 'incorrect'.
    If an incompatible structure is present, rebuild it.
    """
    base = {
        'correct': {field: 0 for field in required_fields},
        'incorrect': {field: 0 for field in required_fields},
    }
    stats = request.session.get('game_stats')
    if not isinstance(stats, dict) or 'correct' not in stats or 'incorrect' not in stats:
        request.session['game_stats'] = base
        return
    # Merge missing fields, keep existing counts where present
    for bucket in ['correct', 'incorrect']:
        if not isinstance(stats.get(bucket), dict):
            stats[bucket] = {}
        for field in required_fields:
            stats[bucket][field] = int(stats[bucket].get(field, 0))
    request.session['game_stats'] = stats


def game_start_view(request):
    categories = Substantiv.objects.values_list('category', flat=True).distinct()
    if request.method == 'POST':
        # set guest flag for this session
        request.session['is_guest'] = bool(request.POST.get('is_guest'))
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


def substantiv_game_view(request):
    if request.method == 'POST':
        # capture guest mode if chosen here
        if request.POST.get('is_guest'):
            request.session['is_guest'] = True
        category = request.POST.get('category', request.session.get('category', 'all'))
        request.session['category'] = category
        print(category)
        # gate: must be authenticated or choose guest
        if not (request.user.is_authenticated or request.session.get('is_guest', False)):
            return render(request, 'choose_mode.html', {
                'post_action': 'substantiv_game',
                'hidden_fields': {'category': category, 'is_guest': '1'},
                'login_next': 'game_start',
                'title': 'Starta Substantiv Spel'
            })
        if category == 'all':
            words = Substantiv.objects.all()
        else:
            words = Substantiv.objects.filter(category=category)
        word = random.choice(words)
        request.session['current_word_num'] = word.number
        return render(request, 'substantiv_game.html', {'word': word, 'category': category})
    else:
        return redirect('substantiv_game')


def substantiv_results_view(request):
    if request.method == 'POST':
        user = request.user
        category = request.session.get('category')
        print(category)
        word_number = request.session.get('current_word_num')
        word = Substantiv.objects.get(number=word_number)
        
        def normalize_text(value):
            if value is None:
                return ''
            normalized = unicodedata.normalize('NFC', value)
            collapsed_spaces = ' '.join(normalized.split())
            return collapsed_spaces.casefold()
        answers = {
            'engelska': request.POST.get('engelska'),
            'obestamt_singular': request.POST.get('obestamt_singular'),
            'bestamt_singular': request.POST.get('bestamt_singular'),
            'obestamt_plural': request.POST.get('obestamt_plural'),
            'bestamt_plural': request.POST.get('bestamt_plural'),
        }
        results = {
            'engelska_result': normalize_text(word.engelska) == normalize_text(answers['engelska']),
            'obestamt_singular_result': normalize_text(word.obestamt_singular) == normalize_text(answers['obestamt_singular']),
            'bestamt_singular_result': normalize_text(word.bestamt_singular) == normalize_text(answers['bestamt_singular']),
            'obestamt_plural_result': normalize_text(word.obestamt_plural) == normalize_text(answers['obestamt_plural']),
            'bestamt_plural_result': normalize_text(word.bestamt_plural) == normalize_text(answers['bestamt_plural']),
        }
        substantiv_fields = ['engelska', 'obestamt_singular', 'bestamt_singular', 'obestamt_plural', 'bestamt_plural']
        ensure_game_stats(request, substantiv_fields)
        
        for field, result in results.items():
            field_name = field.replace('_result', '')

            # Only update profile stats if not a guest and authenticated
            if request.user.is_authenticated and not request.session.get('is_guest', False):
                user.update_record(result, field_name)

            if result:
                request.session['game_stats']['correct'][field_name] += 1
            else:
                request.session['game_stats']['incorrect'][field_name] += 1
        
        if request.user.is_authenticated and not request.session.get('is_guest', False):
            user.update_total(word)
            user.save()
        
        request.session.modified = True
        print(answers)
        print(request.session['game_stats'])
        return render(request, 'substantiv_results.html', {'word': word, 
                                                           'answers': answers, 
                                                           'results': results,
                                                           'game_stats': request.session['game_stats'], 
                                                           'category': category
                                                           })
    else:
        return redirect('substantiv_game')
    

def substantiv_next_question_view(request):
    if request.method == 'POST':
        # Retrieve the category from the POST data
        category = request.POST.get('category')

        # Store the category in the session to ensure it is retained
        request.session['category'] = category

        # Redirect to the game view
        return redirect('substantiv_game')

    # Redirect to the start page if the request method is not POST
    return redirect('game_start')


def substantiv_quit_view(request):
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


def verb_game_view(request):
    if request.method == 'POST':
        # capture guest mode if chosen here
        if request.POST.get('is_guest'):
            request.session['is_guest'] = True
        # gate: must be authenticated or choose guest
        if not (request.user.is_authenticated or request.session.get('is_guest', False)):
            return render(request, 'choose_mode.html', {
                'post_action': 'verb_game',
                'hidden_fields': {},
                'login_next': 'game_start',
                'title': 'Starta Verb Spel'
            })
        words = Verb.objects.all()
        word = random.choice(words)
        request.session['current_word_num'] = word.number
        return render(request, 'verb_game.html', {'word': word})


def verb_results_view(request):
    if request.method == 'POST':
        user = request.user
        word_number = request.session.get('current_word_num')
        word = Verb.objects.get(number=word_number)
        
        def normalize_text(value):
            if value is None:
                return ''
            normalized = unicodedata.normalize('NFC', value)
            collapsed_spaces = ' '.join(normalized.split())
            return collapsed_spaces.casefold()
        answers = {
            'engelska': request.POST.get('engelska'),
            'infinitiv': request.POST.get('infinitiv'),
            'presens': request.POST.get('presens'),
            'imperativ': request.POST.get('imperativ'),
            'preteritum': request.POST.get('preteritum'),
            'perfekt': request.POST.get('perfekt'),
            'pluskvamperfekt': request.POST.get('pluskvamperfekt')
        }
        results = {
            'engelska_result': normalize_text(word.engelska) == normalize_text(answers['engelska']),
            'infinitiv_result': normalize_text(word.infinitiv) == normalize_text(answers['infinitiv']),
            'presens_result': normalize_text(word.presens) == normalize_text(answers['presens']),
            'imperativ_result': normalize_text(word.imperativ) == normalize_text(answers['imperativ']),
            'preteritum_result': normalize_text(word.preteritum) == normalize_text(answers['preteritum']),
            'perfekt_result': normalize_text(word.perfekt) == normalize_text(answers['perfekt']),
            'pluskvamperfekt_result': normalize_text(word.pluskvamperfekt) == normalize_text(answers['pluskvamperfekt'])
        }
        verb_fields = ['engelska', 'infinitiv', 'presens', 'imperativ', 'preteritum', 'perfekt', 'pluskvamperfekt']
        ensure_game_stats(request, verb_fields)

        for field, result in results.items():
            field_name = field.replace('_result', '')

            if request.user.is_authenticated and not request.session.get('is_guest', False):
                user.update_record(result, field_name)

            if result:
                request.session['game_stats']['correct'][field_name] += 1
            else:
                request.session['game_stats']['incorrect'][field_name] += 1
        
        if request.user.is_authenticated and not request.session.get('is_guest', False):
            user.update_total(word)
            user.save()
        
        request.session.modified = True
        print(request.session['game_stats'])
        return render(request, 'verb_results.html', {'word': word, 
                                                           'answers': answers, 
                                                           'results': results,
                                                           'game_stats': request.session['game_stats'], 
                                                           })
    else:
        return redirect('verb_game')
    

def verb_next_question_view(request):
    if request.method == 'POST':
        return redirect('substantiv_game')
    return redirect('game_start')


def verb_quit_view(request):
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

    return render(request, 'verb_summary.html', {'game_stats': game_stats})