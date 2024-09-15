from flask import render_template, redirect, request, session, url_for
from app import app
from app.spotify_api import create_spotify_oauth, get_spotify_client, get_album_tracks
from app.sorting import merge_sort, get_next_comparison
import urllib.parse

@app.route('/')
def index():
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
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    return redirect(url_for('index'))

@app.route('/sort', methods=['GET', 'POST'])
def sort():
    if 'token_info' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        album_link = request.form.get('album_link')
        album_id = album_link.split('/')[-1].split('?')[0]
        tracks = get_album_tracks(album_id)
        session['tracks'] = tracks
        session['comparisons'] = {}
        return redirect(url_for('compare'))

    return render_template('sort.html')

@app.route('/compare', methods=['GET', 'POST'])
def compare():
    if 'tracks' not in session:
        return redirect(url_for('sort'))

    tracks = session['tracks']
    comparisons = session['comparisons']

    if request.method == 'POST':
        song1_id = request.form.get('song1_id')
        song2_id = request.form.get('song2_id')
        chosen_id = request.form.get('chosen')
        comparisons[f"{song1_id}:{song2_id}"] = chosen_id
        session['comparisons'] = comparisons

    sorted_tracks = merge_sort(tracks, comparisons)
    if sorted_tracks:
        session['sorted_tracks'] = sorted_tracks
        return redirect(url_for('result'))

    song1, song2 = get_next_comparison(tracks)
    return render_template('compare.html', song1=song1, song2=song2)

@app.route('/result')
def result():
    if 'sorted_tracks' not in session:
        return redirect(url_for('sort'))

    sorted_tracks = session['sorted_tracks']
    return render_template('result.html', tracks=sorted_tracks)