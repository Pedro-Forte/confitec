import os

from flask import Flask 
from asgiref.wsgi import WsgiToAsgi
from .views.top_ten import top_ten_bp


def create_app():

    app = Flask(__name__)
    app.register_blueprint(top_ten_bp)

    @app.get("/api/v1/health")
    def health():
        return {"success": True}, 200

    return app

flask_app = create_app()
app = WsgiToAsgi(flask_app)