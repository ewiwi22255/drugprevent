from flask import Blueprint, jsonify, request
from datetime import datetime, timezone
from bson import ObjectId
from backend.db import get_db

quiz_bp = Blueprint("quiz", __name__)


def _serialize(doc):
    """將 MongoDB document 轉成可 JSON 序列化的 dict。"""
    doc["id"] = str(doc.pop("_id"))
    return doc


# ─────────────────────────────────────────
# GET /api/quiz
# 回傳所有題目（不含正確答案，避免前端作弊）
# ─────────────────────────────────────────
@quiz_bp.route("/quiz", methods=["GET"])
def get_quiz():
    db = get_db()
    questions = list(db.quizzes.find({}, {"correct": 0, "explanation": 0}))
    for q in questions:
        q["id"] = str(q.pop("_id"))
    return jsonify(questions), 200


# ─────────────────────────────────────────
# POST /api/quiz/submit
# Body: { "answers": [1, 0, 1, ...] }
# 回傳: 分數 + 每題解析
# ─────────────────────────────────────────
@quiz_bp.route("/quiz/submit", methods=["POST"])
def submit_quiz():
    db = get_db()
    data = request.get_json()

    if not data or "answers" not in data:
        return jsonify({"error": "缺少 answers 欄位"}), 400

    submitted = data["answers"]          # list[int]
    questions  = list(db.quizzes.find({}))

    if len(submitted) != len(questions):
        return jsonify({"error": f"題數不符，應為 {len(questions)} 題"}), 400

    score   = 0
    results = []
    for q, selected in zip(questions, submitted):
        is_correct = (selected == q["correct"])
        if is_correct:
            score += 1
        results.append({
            "question"   : q["question"],
            "selected"   : selected,
            "correct"    : q["correct"],
            "is_correct" : is_correct,
            "explanation": q["explanation"],
            "category"   : q["category"],
        })

    total      = len(questions)
    percentage = round(score / total * 100)

    # 儲存本次結果至 MongoDB
    db.quiz_results.insert_one({
        "score"     : score,
        "total"     : total,
        "percentage": percentage,
        "answers"   : results,
        "created_at": datetime.now(timezone.utc),
    })

    return jsonify({
        "score"     : score,
        "total"     : total,
        "percentage": percentage,
        "results"   : results,
    }), 200
