from flask import Flask
from config import Config
from flask_session import Session
import redis

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config.from_object(Config)

# Configure server-side session
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.from_url('redis://red-crjv35qj1k6c73fqk01g:6379')

# Initialize the session
Session(app)

from app import routes