from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from hotels.models import Booking
from chatbot.models import ChatProfile
from tourism.models import UserReview

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Use get_or_create to prevent duplicate ChatProfile creation
            # The signals might have already created one
            ChatProfile.objects.get_or_create(
                user=user,
                defaults={
                    'preferred_language': 'en',
                    'interests': 'football'
                }
            )
            
            # Auto login after registration
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to AFCON 2027 Hotel System.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def profile_view(request):
    user = request.user
    bookings = Booking.objects.filter(user=user).order_by('-created_at')[:5]
    reviews = UserReview.objects.filter(user=user).order_by('-created_at')[:5]
    
    # Use get_or_create instead of try/except to ensure profile exists
    chat_profile, created = ChatProfile.objects.get_or_create(
        user=user,
        defaults={
            'preferred_language': 'en',
            'interests': 'football'
        }
    )
    
    context = {
        'user': user,
        'bookings': bookings,
        'reviews': reviews,
        'chat_profile': chat_profile,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    return redirect('profile')