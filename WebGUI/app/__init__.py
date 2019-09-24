from flask import Flask
from WebGUI.config import Config

app = Flask(__name__)
app.config.from_object(Config)

from WebGUI.app import routes
