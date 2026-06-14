"""
POST /api/anonymous
GET /api/anonymous

負責功能：匿名求助留言
Body:
{
    "type": "諮詢",
    "message": "我想匿名詢問..."
}
"""

from flask import Blueprint, jsonify, request
from datetime import datetime, timezone
from backend.db import get_db

anonymous_bp = Blueprint("anonymous", __name__)


@anonymous_bp.route("/anonymous", methods=["POST"])
def submit_anonymous():
    db = get_db()
    data = request.get_json()

    if not data or not data.get("message"):
        return jsonify({
            "success": False,
            "error": "缺少 message 欄位"
        }), 400

    result = db.anonymous_messages.insert_one({
        "type": data.get("type", "其他"),
        "message": data["message"],
        "created_at": datetime.now(timezone.utc),
    })

    return jsonify({
        "success": True,
        "message": "匿名求助已成功送出",
        "id": str(result.inserted_id)
    }), 201


@anonymous_bp.route("/anonymous", methods=["GET"])
def get_anonymous_messages():
    db = get_db()

    messages = list(
        db.anonymous_messages.find(
            {},
            {
                "_id": 0,
                "type": 1,
                "message": 1,
                "created_at": 1
            }
        ).sort("created_at", -1)
    )

    for item in messages:
        if "created_at" in item:
            item["created_at"] = item["created_at"].isoformat()

    return jsonify(messages), 200