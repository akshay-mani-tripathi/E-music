import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def search_spotify(query):
    # Set up the Spotify client
    client_credentials_manager = SpotifyClientCredentials(client_id='11aaedac932d486db4912b5d2489d95b', client_secret='99943eb9f59347f39c893fae8e17c09f')
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Search for tracks based on the query
    results = sp.search(q=query, type='track', limit=10)
    songs = []

    for track in results['tracks']['items']:
        songs.append({
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'url': track['external_urls']['spotify']
        })

    return songs
# spotify_utils.py
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

def get_spotify_client():
    client_credentials_manager = SpotifyClientCredentials(
        client_id="11aaedac932d486db4912b5d2489d95b",
        client_secret="99943eb9f59347f39c893fae8e17c09f"
    )
    return Spotify(client_credentials_manager=client_credentials_manager)

def get_spotify_genres():
    spotify = get_spotify_client()
    # Fetch categories from Spotify
    categories = spotify.categories(limit=10)
    return [category['name'] for category in categories['categories']['items']]

def get_songs_by_genre(genre):
    spotify = get_spotify_client()
    # Search tracks for the genre
    results = spotify.search(q=f'genre:"{genre}"', type='track', limit=20)
    return [
        {'name': track['name'], 'artist': track['artists'][0]['name']}
        for track in results['tracks']['items']
    ]
