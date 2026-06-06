from flask import Blueprint

quiz_bp = Blueprint(
    "quiz",
    __name__
)

@quiz_bp.route("/api/quiz")
def get_quiz():

    return [
        {
            "id": 1,
            "question": "偶爾使用毒品不會上癮？",
            "answer": False
        }
    ]