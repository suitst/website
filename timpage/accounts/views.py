from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, 'logout.html')


def profile_view(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})


def reset_stats_view(request):
    if request.method == 'POST':
        user = request.user

        stat_fields = [
            'total_answered',
            'engelska_correct', 'engelska_incorrect',
            'obestamt_singular_correct', 'obestamt_singular_incorrect',
            'bestamt_singular_correct', 'bestamt_singular_incorrect',
            'obestamt_plural_correct', 'obestamt_plural_incorrect',
            'bestamt_plural_correct', 'bestamt_plural_incorrect'
        ]

        for field in stat_fields:
            setattr(user, field, 0)

        user.save()

        messages.success(request, 'Your statistics have been reset successfully!')

        return redirect('profile')
    
    return redirect('profile')