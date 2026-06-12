"""
POST /api/chat
負責人：洪邑閩

Body: { "message": "使用者輸入文字" }
回傳: { "reply": "Gemini 回應" }
"""
from flask import Blueprint, jsonify, request
from datetime import datetime, timezone
from backend.db import get_db
from backend.config import GEMINI_API_KEY
import google.generativeai as genai

chat_bp = Blueprint("chat", __name__)

# Gemini 初始化（Key 在後端，不暴露給前端）
genai.configure(api_key=GEMINI_API_KEY)
_model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=(
        "你是一位專業的毒品防制輔導員，只回答與毒品防制、心理健康、求助資源相關的問題。"
        "語氣友善、非批判性，回答請使用繁體中文，長度控制在 200 字以內。"
    )
)


@chat_bp.route("/chat", methods=["POST"])
def chat():
    db   = get_db()
    data = request.get_json()

    if not data or not data.get("message"):
        return jsonify({"error": "message 不能為空"}), 400

    user_msg = data["message"]

    response = _model.generate_content(user_msg)
    reply    = response.text

    # 記錄對話至 MongoDB
    db.chat_logs.insert_one({
        "user_message": user_msg,
        "bot_reply"   : reply,
        "created_at"  : datetime.now(timezone.utc),
    })

    return jsonify({"reply": reply}), 200
