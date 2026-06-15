"""
POST /api/anonymous
負責人：許恩維

Body: { "type": "諮詢|轉介|資訊|其他", "message": "..." }
"""
from flask import Blueprint, jsonify, request
from datetime import datetime, timezone
from backend.db import get_db
from backend.agent.safety import assess_risk, CRISIS_BANNER

anonymous_bp = Blueprint("anonymous", __name__)


@anonymous_bp.route("/anonymous", methods=["POST"])
def submit_anonymous():
    db   = get_db()
    data = request.get_json()

    if not data or not data.get("message"):
        return jsonify({"success": False, "error": "message 不能為空"}), 400

    # 安全護欄：對留言分級，高風險者標記（供後續人工優先檢視）
    risk = assess_risk(data["message"])

    db.anonymous_messages.insert_one({
        "type"      : data.get("type", "其他"),
        "message"   : data["message"],
        "risk_level": risk,
        "created_at": datetime.now(timezone.utc),
    })

    resp = {"success": True, "message": "留言已收到，感謝您的回饋"}
    # 高風險：立即把求助專線回給留言者，不讓他空等
    if risk == "crisis":
        resp["crisis_resources"] = CRISIS_BANNER
    return jsonify(resp), 201
