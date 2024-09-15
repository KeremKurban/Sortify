import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import current_app, session, url_for

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=current_app.config['SPOTIFY_CLIENT_ID'],
        client_secret=current_app.config['SPOTIFY_CLIENT_SECRET'],
        redirect_uri=current_app.config['SPOTIFY_REDIRECT_URI'],
        scope='playlist-read-private'
    )

def get_spotify_client():
    token_info = session.get('token_info', None)
    if not token_info:
        raise Exception("User not logged in")
    
    sp_oauth = create_spotify_oauth()
    token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    session['token_info'] = token_info
    return spotipy.Spotify(auth=token_info['access_token'])

def get_album_tracks(album_id):
    sp = get_spotify_client()
    tracks = sp.album_tracks(album_id)
    return [{'id': track['id'], 'name': track['name'], 'artists': [artist['name'] for artist in track['artists']]} for track in tracks['items']]