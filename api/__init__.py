from flask import Flask
from .config import Config
from flask_socketio import SocketIO

socket = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    socket.init_app(app)
    from .news import news
    app.register_blueprint(news)
    return app, socket