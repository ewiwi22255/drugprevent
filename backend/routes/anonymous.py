"""
POST /api/anonymous
負責人：許恩維

Body: { "type": "諮詢|轉介|資訊|其他", "message": "..." }
"""
from flask import Blueprint, jsonify, request
from datetime import datetime, timezone
from backend.db import get_db

anonymous_bp = Blueprint("anonymous", __name__)


@anonymous_bp.route("/anonymous", methods=["POST"])
def submit_anonymous():
    db   = get_db()
    data = request.get_json()

    if not data or not data.get("message"):
        return jsonify({"success": False, "error": "message 不能為空"}), 400

    db.anonymous_messages.insert_one({
        "type"      : data.get("type", "其他"),
        "message"   : data["message"],
        "created_at": datetime.now(timezone.utc),
    })

    return jsonify({"success": True, "message": "留言已收到，感謝您的回饋"}), 201
