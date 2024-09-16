import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
    SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
    
    # Dynamically set the redirect URI based on the environment
    if os.environ.get('RENDER_EXTERNAL_URL'):
        SPOTIFY_REDIRECT_URI = f"{os.environ.get('RENDER_EXTERNAL_URL')}/callback"
    else:
        SPOTIFY_REDIRECT_URI = 'http://localhost:5001/callback'