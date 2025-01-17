from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
import requests
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

def home(request):

    return render(request,"home.html")

def user_login(request): 
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'dashboard')
            messages.success(request, f"Welcome back, {user.username}!")

            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    return render(request, "login.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
             messages.error(request, "Username already exist! Please try another username!")
             return redirect('signup')
        
        if User.objects.filter(email=email):
             messages.error(request, "Email alrady Registered")
             return redirect('signup')
        
        if len(username)>15:
             messages.error(request, "Username must be under 15 characters")
            
        if pass1 != pass2:
             messages.error(request, "Password didn't match")

        if not username.isalnum():
             messages.error(request, "Username must be Alpha-Numeric!")
             return redirect('signup')
    
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your account has been created succesfully.")
        return redirect('login')

    return render(request,"signup.html")

def signout(request):
        logout(request)
        messages.success(request, "Logged out Successfully")
        return redirect('home')

def dashboard(request):
     return render(request,"dashboard.html")

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from .forms import ProfileSettingsForm, CustomPasswordChangeForm
from .models import ProfileSettings, Notification

def settings(request):
    # Get or create the user's profile settings
    profile_settings, created = ProfileSettings.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Handle the profile settings and password forms
        profile_form = ProfileSettingsForm(request.POST, request.FILES, instance=profile_settings)
        password_form = CustomPasswordChangeForm(request.user, request.POST)

        if 'update_profile' in request.POST and profile_form.is_valid():
            # Save the profile settings form (including the profile picture if uploaded)
            old_profile = ProfileSettings.objects.get(id=profile_settings.id)
            profile_form.save()

            # Check for changes in the fields and create notifications
            changes = []
            if old_profile.bio != profile_settings.bio:
                changes.append('Bio')
            if old_profile.location != profile_settings.location:
                changes.append('Location')
            if old_profile.profile_photo != profile_settings.profile_photo:
                changes.append('Profile Picture')

            # If there are changes, create a notification
            if changes:
                message = f"Profile updated successfully! Changed fields: {', '.join(changes)}."
                Notification.objects.create(
                    user=request.user,
                    message=message
                )
                messages.success(request, message)
            else:
                messages.info(request, "No changes were made to your profile.")
            
            return redirect('settings')  # Redirect to prevent resubmission on refresh

        if 'change_password' in request.POST and password_form.is_valid():
            # Change the password and update the session to keep the user logged in
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            messages.success(request, "Password changed successfully!")
            return redirect('settings')  # Redirect after password change

    else:
        # For GET requests, initialize the forms with the current user's data
        profile_form = ProfileSettingsForm(instance=profile_settings)
        password_form = CustomPasswordChangeForm(request.user)

    # Render the settings page with the forms
    return render(request, 'settings.html', {
        'profile_form': profile_form,
        'password_form': password_form
    })

def profile(request):
     return render(request,"profile.html")

def helpcenter(request):
    return render(request,"helpcenter.html")
def contact(request):
     return render(request,"contact.html")
def subscription(request):
     return render(request,"subscription.html")
def about_us(request):
     return render(request, "about_us.html")
def process_voice(request):
     return render(request,"process_voice.html")
def search(request):
    query = request.GET.get('query', '')  # Get the search query from the URL parameters
    songs = []

    if query:
        # Authenticate with Spotify
        auth_response = requests.post(
            'https://accounts.spotify.com/api/token',
            {
                'grant_type': 'client_credentials',
                'client_id': '11aaedac932d486db4912b5d2489d95b',
                'client_secret': '99943eb9f59347f39c893fae8e17c09f',
            }
        )
        auth_data = auth_response.json()
        access_token = auth_data['access_token']

        # Perform the search query
        headers = {'Authorization': f'Bearer {access_token}'}
        search_url = f'https://api.spotify.com/v1/search?q={query}&type=track&limit=10'
        response = requests.get(search_url, headers=headers)
        data = response.json()

        # Extract relevant song information
        songs = [
            {
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'album': track['album']['name'],
                'preview_url': track['preview_url'],
                'external_url': track['external_urls']['spotify'],
            }
            for track in data.get('tracks', {}).get('items', [])
        ]

    return render(request, 'search.html', {'songs': songs, 'query': query})

# views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def profile_view(request):
     return render(request,"profile.html")
@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    notifications.update(is_read=True)  # Mark all notifications as read
    return render(request, 'notifications.html', {'notifications': notifications})
import speech_recognition as sr
from django.shortcuts import render
from .spotify_helper import search_spotify

def voice_search(request):
    if request.method == "POST":
        query = request.POST.get('query')
        
        if query:
            # Search for songs on Spotify with the voice query
            results = search_spotify(query)
            return render(request, 'voice_results.html', {'songs': results, 'query': query})
        else:
            return render(request, 'voice_results.html', {'error': "No query received."})
    
    return render(request, 'voice_search.html')
from django.shortcuts import render
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Initialize Spotify API (replace with your credentials)
SPOTIFY_CLIENT_ID = 'your_spotify_client_id'
SPOTIFY_CLIENT_SECRET = 'your_spotify_client_secret'

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
))

def genres_page(request):
    genres = ['Hindi', 'English', 'Punjabi', 'Tamil']
    return render(request, 'genres.html', {'genres': genres})

def genre_songs(request, genre_name):
    # Fetch songs based on the genre
    if genre_name == 'Hindi':
        query = 'Bollywood'
    elif genre_name == 'English':
        query = 'Pop'
    elif genre_name == 'Punjabi':
        query = 'Punjabi'
    elif genre_name == 'Tamil':
        query = 'Tamil'
    else:
        query = 'Top Hits'

    results = spotify.search(q=query, type='track', limit=10)
    songs = results['tracks']['items']

    return render(request, 'genre_songs.html', {'genre_name': genre_name, 'songs': songs})
