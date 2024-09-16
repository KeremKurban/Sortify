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
            album = sp.album(album_id)
            tracks = album['tracks']['items']
            album_cover = album['images'][0]['url']
            return [{'id': track['id'], 'name': track['name'], 'artists': [artist['name'] for artist in track['artists']], 'preview_url': track['preview_url'], 'album_cover': album_cover} for track in tracks]
        elif 'playlist' in link:
            playlist_id = link.split('/')[-1].split('?')[0]
            playlist = sp.playlist(playlist_id)
            tracks = playlist['tracks']['items']
            album_cover = playlist['images'][0]['url'] if playlist['images'] else None
            return [{'id': track['track']['id'], 'name': track['track']['name'], 'artists': [artist['name'] for artist in track['track']['artists']], 'preview_url': track['track']['preview_url'], 'album_cover': album_cover} for track in tracks]
        else:
            return []
    except spotipy.exceptions.SpotifyException as e:
        print(f"Error fetching tracks: {e}")
        return []