from flask import Flask
from config import Config
from flask_session import Session
import redis

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config.from_object(Config)

# Initialize the session
Session(app)

from app import routes