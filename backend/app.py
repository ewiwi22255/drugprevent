from flask import Flask
from flask_cors import CORS

from routes.anonymous import anonymous_bp
from routes.quiz import quiz_bp

app = Flask(__name__)

CORS(app)

app.register_blueprint(
    anonymous_bp
)

app.register_blueprint(
    quiz_bp
)

@app.route("/")
def home():
    return {
        "message": "Backend Running"
    }

if __name__ == "__main__":
    app.run(debug=True)