from flask import render_template, redirect, request, session, url_for, render_template_string
from app import app
from app.spotify_api import create_spotify_oauth, get_spotify_client, get_tracks_from_spotify, create_spotify_client  # Import create_spotify_client
from app.sorting import merge_sort, get_next_comparison
import urllib.parse

@app.route('/')
def index():
    print("Rendering index.html")  # Debug print
    return render_template('index.html')

@app.route('/login')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    print(f"Received code: {code}")  # Debug print
    if not code:
        return "Error: No code provided", 400
    token_info = sp_oauth.get_access_token(code)
    print(f"Token info: {token_info}")  # Debug print
    if not token_info:
        return "Error: Unable to retrieve token", 400
    session["token_info"] = token_info
    return redirect(url_for('sort'))  # Redirect to sort page

@app.route('/sort', methods=['GET', 'POST'])
def sort():
    if request.method == 'POST':
        link = request.form.get('album_link')
        sp = create_spotify_client()  # Use the client credentials flow
        tracks = get_tracks_from_spotify(link, sp)  # Pass the Spotify client
        if not tracks:
            return "Error: Unable to fetch tracks", 400
        session['tracks'] = tracks
        session['comparisons'] = {}
        session['total_comparisons'] = (len(tracks) * (len(tracks) - 1)) // 2
        session['completed_comparisons'] = 0
        print(f"Tracks: {tracks}")  # Debug print
        return redirect(url_for('compare'))

    return render_template('sort.html')

@app.route('/compare', methods=['GET', 'POST'])
def compare():
    tracks = session.get('tracks', [])
    comparisons = session.get('comparisons', {})
    total_comparisons = session.get('total_comparisons', 1)
    completed_comparisons = session.get('completed_comparisons', 0)

    if request.method == 'POST':
        song1_id = request.form.get('song1_id')
        song2_id = request.form.get('song2_id')
        chosen_id = request.form.get('chosen')
        print(f"Received comparison: {song1_id} vs {song2_id}, chosen: {chosen_id}")  # Debug print
        comparison_key = f"{song1_id}:{song2_id}"
        comparisons[comparison_key] = chosen_id
        session['comparisons'] = comparisons
        session['completed_comparisons'] = completed_comparisons + 1
        print(f"Updated comparisons: {session['comparisons']}")  # Debug print

    song1, song2 = get_next_comparison(tracks, comparisons)
    if song1 is None or song2 is None:
        sorted_tracks = merge_sort(tracks, comparisons)
        session['tracks'] = sorted_tracks
        return redirect(url_for('result'))

    progress = (completed_comparisons / total_comparisons) * 100
    album_cover = tracks[0].get('album_cover') if tracks else None
    return render_template('compare.html', song1=song1, song2=song2, progress=progress, album_cover=album_cover)

@app.route('/result')
def result():
    tracks = session.get('tracks', [])
    return render_template('result.html', tracks=tracks)

@app.route('/test_static')
def test_static():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Test Static</title>
        <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    </head>
    <body>
        <h1>Static File Test</h1>
        <p>If the CSS is loaded correctly, this text should be styled.</p>
    </body>
    </html>
    ''')

def get_album_tracks(album_id, sp):
    tracks = sp.album_tracks(album_id)
    return [{'id': track['id'], 'name': track['name'], 'artists': [artist['name'] for artist in track['artists']]} for track in tracks['items']]