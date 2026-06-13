"""
POST /api/chat        — 傳送訊息給 Agent
GET  /api/chat/<sid>  — 取得指定 session 的對話歷史
DELETE /api/chat/<sid>— 清除 session

負責人：洪邑閩
"""
import uuid
from flask import Blueprint, jsonify, request
from datetime import datetime, timezone
from backend.db import get_db
from backend.agent.runner import run_agent

chat_bp = Blueprint("chat", __name__)


def _now():
    return datetime.now(timezone.utc)


# ── POST /api/chat ─────────────────────────────────────────────────────────────

@chat_bp.route("/chat", methods=["POST"])
def chat():
    db   = get_db()
    data = request.get_json()

    if not data or not data.get("message"):
        return jsonify({"error": "message 不能為空"}), 400

    user_message = data["message"]
    session_id   = data.get("session_id") or str(uuid.uuid4())

    # 讀取該 session 的歷史對話
    session  = db.chat_sessions.find_one({"session_id": session_id})
    history  = session["messages"] if session else []

    # 加入本次使用者訊息
    history.append({"role": "user", "content": user_message})

    try:
        reply = run_agent(history)
    except Exception as e:
        print("【Agent 錯誤】:", str(e))
        return jsonify({"error": str(e)}), 500

    # 加入 assistant 回覆
    history.append({"role": "assistant", "content": reply})

    # 存回 MongoDB（upsert）
    db.chat_sessions.update_one(
        {"session_id": session_id},
        {
            "$set": {
                "messages"  : history,
                "updated_at": _now(),
            },
            "$setOnInsert": {"created_at": _now()},
        },
        upsert=True,
    )

    return jsonify({
        "reply"     : reply,
        "session_id": session_id,
    }), 200


# ── GET /api/chat/<session_id> ────────────────────────────────────────────────

@chat_bp.route("/chat/<session_id>", methods=["GET"])
def get_history(session_id):
    db      = get_db()
    session = db.chat_sessions.find_one(
        {"session_id": session_id},
        {"_id": 0, "session_id": 1, "messages": 1, "updated_at": 1},
    )
    if not session:
        return jsonify({"error": "找不到該 session"}), 404

    return jsonify(session), 200


# ── DELETE /api/chat/<session_id> ─────────────────────────────────────────────

@chat_bp.route("/chat/<session_id>", methods=["DELETE"])
def clear_session(session_id):
    db     = get_db()
    result = db.chat_sessions.delete_one({"session_id": session_id})
    if result.deleted_count == 0:
        return jsonify({"error": "找不到該 session"}), 404

    return jsonify({"success": True, "message": "對話已清除"}), 200
