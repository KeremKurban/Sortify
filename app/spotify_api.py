import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from flask import current_app, session, url_for

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=current_app.config['SPOTIFY_CLIENT_ID'],
        client_secret=current_app.config['SPOTIFY_CLIENT_SECRET'],
        redirect_uri=current_app.config['SPOTIFY_REDIRECT_URI'],
        scope='playlist-read-private'
    )

def create_spotify_client():
    client_credentials_manager = SpotifyClientCredentials(
        client_id=current_app.config['SPOTIFY_CLIENT_ID'],
        client_secret=current_app.config['SPOTIFY_CLIENT_SECRET']
    )
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_spotify_client():
    token_info = session.get('token_info', None)
    if not token_info:
        raise Exception("User not logged in")
    
    sp_oauth = create_spotify_oauth()
    token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    session['token_info'] = token_info
    return spotipy.Spotify(auth=token_info['access_token'])


def get_tracks_from_spotify(link, sp):
    try:
        if 'album' in link:
            album_id = link.split('/')[-1].split('?')[0]
            tracks = sp.album_tracks(album_id)
            return [{'id': track['id'], 'name': track['name'], 'artists': [artist['name'] for artist in track['artists']]} for track in tracks['items']]
        elif 'playlist' in link:
            playlist_id = link.split('/')[-1].split('?')[0]
            tracks = sp.playlist_tracks(playlist_id)
            return [{'id': track['track']['id'], 'name': track['track']['name'], 'artists': [artist['name'] for artist in track['track']['artists']]} for track in tracks['items']]
        else:
            return []
    except spotipy.exceptions.SpotifyException as e:
        print(f"Error fetching tracks: {e}")
        return []