import os

from flask import Flask 
from asgiref.wsgi import WsgiToAsgi

def create_app():

    app = Flask(__name__)

    @app.get("/api/v1/health")
    def health():
        return {"success": True}, 200

    @app.route("/swagger.json")
    def swagger_json():
        static_dir = os.path.join(app.root_path, "../static")
        return send_from_directory(static_dir, "swagger.json")

    return app

flask_app = create_app()
app = WsgiToAsgi(flask_app)