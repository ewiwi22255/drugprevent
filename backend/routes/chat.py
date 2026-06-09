"""
POST /api/chat
負責人：洪邑閩
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
    model_name="gemini-2.5-flash",
    system_instruction=(
        "你是一個反毒與防範犯罪的宣導助手，專門回答毒品防制、心理健康、求助資源相關問題。"
        "語氣友善、非批判性，請使用繁體中文回覆，長度控制在 200 字以內。"
    )
)


@chat_bp.route("/chat", methods=["POST"])
def chat():
    db = get_db()
    data = request.get_json()

    if not data or not data.get("message"):
        return jsonify({"error": "沒有輸入訊息"}), 400

    user_message = data["message"]

    try:
        response = _model.generate_content(user_message)
        reply = response.text
    except Exception as e:
        print("【Gemini 錯誤】:", str(e))
        return jsonify({"error": str(e)}), 500

    # 記錄對話至 MongoDB
    db.chat_logs.insert_one({
        "user_message": user_message,
        "bot_reply"   : reply,
        "created_at"  : datetime.now(timezone.utc),
    })

    return jsonify({"reply": reply}), 200
