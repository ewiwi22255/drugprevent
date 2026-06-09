import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from backend.config import DEBUG

from backend.routes.quiz       import quiz_bp
from backend.routes.resources  import resources_bp
from backend.routes.anonymous  import anonymous_bp
from backend.routes.chat       import chat_bp
from backend.routes.prevention import prevention_bp
from backend.routes.stats      import stats_bp

# 前端靜態檔案放在專案根目錄
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def create_app():
    app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
    CORS(app)

    app.register_blueprint(quiz_bp,       url_prefix="/api")
    app.register_blueprint(resources_bp,  url_prefix="/api")
    app.register_blueprint(anonymous_bp,  url_prefix="/api")
    app.register_blueprint(chat_bp,       url_prefix="/api")
    app.register_blueprint(prevention_bp, url_prefix="/api")
    app.register_blueprint(stats_bp,      url_prefix="/api")

    # 根路徑與其他非 /api 路徑都回傳 index.html
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_frontend(path):
        target = os.path.join(FRONTEND_DIR, path)
        if path and os.path.exists(target):
            return send_from_directory(FRONTEND_DIR, path)
        return send_from_directory(FRONTEND_DIR, "index.html")

    return app
