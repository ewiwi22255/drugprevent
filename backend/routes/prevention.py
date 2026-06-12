"""
POST /api/prevention/submit
負責人：洪邑閩

Body: {
  "scores": {
    "成癮與生理機制": 6,
    "藥物迷思辨析": 4,
    "誘因與環境辨識": 8,
    "復健與心理觀念": 7
  }
}
"""
from flask import Blueprint, jsonify, request
from datetime import datetime, timezone
from backend.db import get_db

prevention_bp = Blueprint("prevention", __name__)


@prevention_bp.route("/prevention/submit", methods=["POST"])
def submit_prevention():
    db   = get_db()
    data = request.get_json()

    if not data or "scores" not in data:
        return jsonify({"error": "缺少 scores 欄位"}), 400

    db.prevention_results.insert_one({
        "scores"    : data["scores"],
        "created_at": datetime.now(timezone.utc),
    })

    return jsonify({"success": True}), 201
