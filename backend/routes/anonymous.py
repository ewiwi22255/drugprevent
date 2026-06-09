"""
POST /api/anonymous
負責人：許恩維
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

    return jsonify({"success": True, "message": "送出成功"}), 201
