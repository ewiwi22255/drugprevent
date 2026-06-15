from backend.app import create_app
from backend.config import DEBUG

app = create_app()

if __name__ == "__main__":
    app.run(debug=DEBUG, port=5000, use_reloader=False)
