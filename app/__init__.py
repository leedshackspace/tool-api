#app/__init__.py
#Flask app initialisation

from flask import Flask

app = Flask(__name__, instance_relative_config=True)

from app import views

app.config.from_object('config')
